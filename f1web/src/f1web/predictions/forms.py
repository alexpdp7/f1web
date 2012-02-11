from django.forms import ModelForm
from f1web.predictions.models import Prediction

class PredictionForm(ModelForm):
    class Meta:
        model = Prediction
        exclude = ('user', 'race', 'top_ten',)
