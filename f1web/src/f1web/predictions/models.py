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

class ScoredPrediction(models.Model):
    prediction = models.OneToOneField(Prediction, primary_key=True)
    correct_pole = models.IntegerField()
    correct_fastest_lap = models.IntegerField()
    correct_names_among_top_10 = models.IntegerField()
    correct_names_among_top_3 = models.IntegerField()
    correct_finishing_position = models.IntegerField()
    correct_teams = models.IntegerField()
    correct_winner = models.IntegerField()
    total = models.IntegerField()
    
    class Meta:
        db_table = 'v_predictions_predictionresult'
