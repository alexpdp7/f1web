from django.shortcuts import render
from f1web.championship.models import Race
from f1web.predictions.forms import PredictionForm
from f1web.predictions.models import Prediction, PredictionPosition
from datetime import date
from django.forms.models import modelformset_factory

def index(request):
    return render(request, 'predictions/index.html')

def race(request, championship, race_code):
    race = Race.objects.get(championship=championship, code=race_code)
    prediction_form = None
    
    if race.date > date.today() and request.user.is_authenticated():
        user_race_predictions = Prediction.objects.filter(race=race, user=request.user)
        
        if user_race_predictions.count() > 0:
            prediction = user_race_predictions.all()[0]
        else: 
            prediction = Prediction(user=request.user,race=race)
        
        if request.POST:
            prediction_form = PredictionForm(request.POST, instance = prediction)
            if prediction_form.is_valid():
                prediction_form.save()
        else:
            prediction_form = PredictionForm(instance = prediction)
            
        TopTenFormSet = modelformset_factory(
            PredictionPosition, 
            extra=10,
            max_num=10,
            exclude=('prediction',)
            )
        
        top_ten = TopTenFormSet(request.POST if request.POST else None, queryset=PredictionPosition.objects.filter(prediction=prediction))
        
        if request.POST:
            prediction_positions = top_ten.save(commit=False)
            for prediction_position in prediction_positions:
                prediction_position.prediction = prediction
                prediction_position.save()

    return render(request, 'predictions/race.html', {
        'race': race,
        'prediction_form': prediction_form, 
        'top_ten': top_ten,
    })
