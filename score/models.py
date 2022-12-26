from django.db import models
from django.contrib.auth.models import User

class Score(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    score_a = models.IntegerField()
    score_b = models.IntegerField()
    score_c = models.IntegerField()