from django.forms.models import ModelChoiceField

class position_formfield_callback():
    def __init__(self, race):
        self.race = race
    
    def __call__(self,f, **kwargs):
        if f.attname in ('driver_id', 'pole_position_id', 'fastest_lap_id'):
            return ModelChoiceField(self.race.get_drivers().order_by('code'))
        else:
            return f.formfield(**kwargs)
