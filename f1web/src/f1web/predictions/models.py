from django.db import models
from django.contrib.auth.models import User
from f1web.championship.models import Race, Driver

class Prediction(models.Model):
    user = models.ForeignKey(User)
    race = models.ForeignKey(Race)
    pole_position = models.ForeignKey(Driver, related_name='+')
    fastest_lap = models.ForeignKey(Driver, related_name='+')
    top_ten = models.ManyToManyField(Driver, through='PredictionPosition')

class PredictionPosition(models.Model):
    prediction = models.ForeignKey(Prediction)
    position = models.IntegerField(choices=zip(range(1,11), range(1,11)))
    driver = models.ForeignKey(Driver)
