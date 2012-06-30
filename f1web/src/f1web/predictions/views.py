from django.shortcuts import render
from f1web.championship.models import Race
from f1web.predictions.forms import position_formfield_callback
from f1web.predictions.models import Prediction, PredictionPosition, get_scores_table
from f1web.predictions.calculator import calculate
from datetime import date
from django.forms.models import modelformset_factory, modelform_factory

def index(request):
    return render(request, 'predictions/index.html', {
        'scores_table': get_scores_table(),
    })

def race(request, championship, race_code):
    race = Race.objects.get(championship=championship, code=race_code)
    user_race_predictions = Prediction.objects.filter(race=race, user=request.user)

    if race.date > date.today() and request.user.is_authenticated():
        if user_race_predictions.count() > 0:
            prediction = user_race_predictions.all()[0]
        else: 
            prediction = Prediction(user=request.user,race=race)
        
        PredictionForm = modelform_factory(
            Prediction, 
            exclude=('user', 'race', 'top_ten',), 
            formfield_callback=position_formfield_callback(race))
        
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
            exclude=('prediction',),
            formfield_callback=position_formfield_callback(race),
            )
        
        top_ten = TopTenFormSet(
            request.POST if request.POST else None, 
            queryset=PredictionPosition.objects.filter(prediction=prediction),
            initial=[{'position': position} for position in range(1,11)]
            )
        
        if request.POST:
            prediction_positions = top_ten.save(commit=False)
            for prediction_position in prediction_positions:
                prediction_position.prediction = prediction
                prediction_position.save()

        return render(request, 'predictions/race_enter_prediction.html', {
            'race': race,
            'prediction_form': prediction_form, 
            'top_ten': top_ten,
        })
    else:
        if user_race_predictions.exists():
            prediction = user_race_predictions.all()[0]
            prediction_calculation = calculate(prediction)
            return render(request, 'predictions/race_view_prediction.html', {
                'race': race,
                'prediction': prediction, 
                'prediction_calculation': prediction_calculation,
            })
