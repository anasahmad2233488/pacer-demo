import logging
import pendulum

from airflow.decorators import task
from airflow.models.dag import DAG

import boto3
import botocore
import os
import datetime
import json
import random

from sqlalchemy import create_engine
from sqlalchemy import event

logger = logging.getLogger('airflow.task')

postgresql_engine = create_engine(
    "postgresql+psycopg2://doadmin:AVNS_zvzNm1a_S7s72eZFR0Y@db-postgresql-sgp1-58466-do-user-5054460-0.b.db.ondigitalocean.com:25060/defaultdb",    
    pool_reset_on_return=None, # disable default reset-on-return scheme
)


session = boto3.session.Session()
client_params={
        'endpoint_url': 'https://sgp1.digitaloceanspaces.com',
        'config': botocore.config.Config(s3={'addressing_style': 'virtual'}), 
        'region_name': 'sgp1', 
        'aws_access_key_id': 'DO00QE36P8F2AB3EBLHQ', 
        'aws_secret_access_key': 'zEiv8fKfWc7LQ+3gwUrfBJnRwxASQulCJWBfmeNCK24'
    }



@task(task_id="load_data")
def load_data():
    client = session.client('s3', **client_params)
    conn = postgresql_engine.connect()
    response = client.list_objects(Bucket='fukiage-space', Prefix='device-data/data')

    if 'Contents'not in response.keys():
        return []

    files = response['Contents']
    clean_up = []
    for fn in files:
        target_file = '/home/airflow/dags/temp2.json'
        client.download_file(Key=fn['Key'], Bucket='fukiage-space', Filename=target_file)
        with open(target_file, 'rb') as f:
            data = json.loads(f.read())
        os.remove(target_file)

        device_data = data['device_data']

        for d in device_data:
            device = d['device_name']
            dt = d['datetime'].split('.')[0]
            d1 = d['d1']
            d2 = d['d2']

            statement = """INSERT INTO dw.device_data (device_name, datetime, d1, d2)
            VALUES ('{}', '{}', {}, {})""".format(device, dt, d1, d2)

            conn.execute(statement)
        
        clean_up.append(fn['Key'])

    conn.close()
    return clean_up


@task(task_id="cleanup")
def cleanup(files):
    client = session.client('s3', **client_params)
    for fn in files:
        target_fn = fn.replace('device-data', 'device-data-archive')
        client.copy_object(Bucket='fukiage-space', CopySource='fukiage-space/{}'.format(fn), Key=target_fn)
        client.delete_object(Bucket='fukiage-space', Key=fn)


with DAG(
    schedule_interval='0 * * * *',
    catchup=False,
    dagrun_timeout=datetime.timedelta(minutes=120),
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    dag_id='Load_Device_Data'
    ) as dag:    

    ff = load_data()
    cleanup(ff)
