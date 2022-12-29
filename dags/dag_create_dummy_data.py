import logging
import boto3
import botocore
import datetime
import json
import random
import pendulum

from airflow.decorators import task
from airflow.models.dag import DAG

logger = logging.getLogger('airflow.task')


@task(task_id="generate_dummy_data")
def generate_dummy_data():
    now = str(datetime.datetime.now())

    fn_now = now
    for symbol in ['-', ' ', '.', ':']:
        fn_now = fn_now.replace(symbol, '')

    data = {
        'device_data':[
                {'device_name': 'device1', 'datetime': now, 'd1': random.random()*100,  'd2':random.random()*100},
                {'device_name': 'device2', 'datetime': now, 'd1': random.random()*100,  'd2':random.random()*100},
                {'device_name': 'device3', 'datetime': now, 'd1': random.random()*100,  'd2':random.random()*100},
                {'device_name': 'device4', 'datetime': now, 'd1': random.random()*100,  'd2':random.random()*100},
                {'device_name': 'device5', 'datetime': now, 'd1': random.random()*100,  'd2':random.random()*100},
            ]

        }

    json_data = json.dumps(data)

    session = boto3.session.Session()
    client = session.client('s3',
                            endpoint_url='https://sgp1.digitaloceanspaces.com',
                            config=botocore.config.Config(s3={'addressing_style': 'virtual'}), 
                            region_name='sgp1', 
                            aws_access_key_id='DO00QE36P8F2AB3EBLHQ', 
                            aws_secret_access_key='zEiv8fKfWc7LQ+3gwUrfBJnRwxASQulCJWBfmeNCK24')

    client.put_object(Bucket='fukiage-space', 
                      Key="device-data/data-{}.json".format(fn_now), 
                      Body=json_data, 
                      ACL='private',
                    )
        

with DAG(
    schedule_interval='*/15 * * * *',
    catchup=False,
    dagrun_timeout=datetime.timedelta(minutes=120),
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    dag_id='Generate_Dummy_Data'
    ) as dag:    
    generate_dummy_data()
