import formative
from django.conf.urls import include, url
from django.contrib import admin

admin.autodiscover()
formative.autodiscover()

urlpatterns = [
    url(r'^admin/', include(admin.site.urls))
]
