from django.urls import path

from . import views

app_name = 'passphrase_api'
urlpatterns = [
    path('/basic', views.BasicValidationView.as_view(), name='basic_validation'),
]
