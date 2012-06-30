from django.db import models
from django.contrib.auth.models import User
from f1web.championship.models import Race, Driver
from django.db import connection
from f1web.commons.sql import dictfetchall
from collections import defaultdict

class Prediction(models.Model):
    user = models.ForeignKey(User)
    race = models.ForeignKey(Race)
    pole_position = models.ForeignKey(Driver, related_name='+')
    fastest_lap = models.ForeignKey(Driver, related_name='+')
    top_ten = models.ManyToManyField(Driver, through='PredictionPosition')
    
    class Meta:
        unique_together = ['user', 'race',]

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

def get_scores_table():
    cursor = connection.cursor()

    cursor.execute("""
        select   auth_user.username, 
                 championship_race.name, 
                 championship_race.date, 
                 total, sum(total) over (partition by user_id order by championship_race.date) as total_acc 
        from     v_predictions_predictionresult 
        join     predictions_prediction on v_predictions_predictionresult.prediction_id = predictions_prediction.id 
        join     auth_user on predictions_prediction.user_id = auth_user.id 
        join     championship_race on predictions_prediction.race_id = championship_race.id 
        order by championship_race.date
    """)
    scores_table_raw = dictfetchall(cursor)
    pivoted_scores = defaultdict(dict)

    for score_entry in scores_table_raw:
        race_entry = pivoted_scores[(score_entry['date'], score_entry['name'])]
        race_entry[score_entry['username']] = { 'total': score_entry['total'], 'total_acc': score_entry['total_acc']}
        
    return sorted(pivoted_scores.items())
