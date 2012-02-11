from django.shortcuts import render
from f1web.championship.models import Race
from f1web.predictions.forms import PredictionForm
from f1web.predictions.models import Prediction
from datetime import date

def index(request):
    return render(request, 'predictions/index.html')

def race(request, championship, race_code):
    race = Race.objects.get(championship=championship, code=race_code)
    prediction_form = None
    
    if race.date > date.today() and request.user.is_authenticated():
        user_race_prediction = Prediction.objects.filter(race=race, user=request.user)
        
        if user_race_prediction.count() > 0:
            prediction = user_race_prediction.all()[0]
        else: 
            prediction = Prediction(user=request.user,race=race)
        
        if request.POST:
            prediction_form = PredictionForm(request.POST, instance = prediction)
            if prediction_form.is_valid():
                prediction_form.save()
        else:
            prediction_form = PredictionForm(instance = prediction)
    
    return render(request, 'predictions/race.html', {
        'race': race,
        'prediction_form': prediction_form, 
    })
