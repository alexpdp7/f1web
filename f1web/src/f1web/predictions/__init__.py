from django.conf.urls.defaults import *
from f1web.championship.models import Race

urls = patterns('',
    (r'^$', 'f1web.predictions.views.index'),
    (r'^login.html$', 'django.contrib.auth.views.login'),
    (r'^logout$', 'django.contrib.auth.views.logout'),
    (r'^races.html$', 'django.views.generic.list_detail.object_list', {
        'queryset': Race.objects.all(),
        'template_name': 'predictions/races.html',
    }, 'races'),
    (r'^race/(?P<championship>\d{4})/(?P<race_code>\w{3}).html$', 'f1web.predictions.views.race')
)
