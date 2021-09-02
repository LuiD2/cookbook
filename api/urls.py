from django.conf.urls import url
import api.views


urlpatterns = [
    url(r'^menu$', api.views.menu_api),
    url(r'^menu/([0-9]+)$', api.views.menu_api)
]
