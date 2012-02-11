from django.conf.urls.defaults import *

urls = patterns('',
    (r'^$', 'f1web.predictions.views.index'),
    (r'^login.html$', 'django.contrib.auth.views.login'),
    (r'^logout$', 'django.contrib.auth.views.logout'),
)
