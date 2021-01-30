from django.urls import path, include
from rest_framework import routers

from . import views

router = routers.DefaultRouter(trailing_slash=False)
router.include_format_suffixes = False
router.register('basic', views.BasicValidationViewSet, basename='basic_validation')
router.register('advanced', views.AdvancedValidationViewSet, basename='advanced_validation')

app_name = 'passphrase_api'
urlpatterns = [
    path('', include(router.urls)),
]
