from django.conf.urls.defaults import *
from f1web.championship.models import Race
from django.views.generic import ListView

class RaceListView(ListView):
    model = Race
    template_name = 'predictions/races.html'

urls = patterns('',
    (r'^$', 'f1web.predictions.views.index'),
    (r'^login.html$', 'django.contrib.auth.views.login'),
    (r'^logout$', 'django.contrib.auth.views.logout'),
    (r'^races.html$', RaceListView.as_view(), {}, 'races'),
    (r'^race/(?P<championship>\d{4})/(?P<race_code>\w{3}).html$', 'f1web.predictions.views.race')
)
