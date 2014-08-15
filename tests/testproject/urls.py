import formative
from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()
formative.autodiscover()
urlpatterns = patterns('', url(r'^admin/', include(admin.site.urls)),)
