from django.conf.urls import patterns, include, url

from f1web import predictions

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'f1web.views.home', name='home'),
    # url(r'^f1web/', include('f1web.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include(predictions.urls))
)
