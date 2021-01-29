from django.urls import path, include
from rest_framework import routers

from . import views

router = routers.DefaultRouter(trailing_slash=False)
router.include_format_suffixes = False

app_name = 'passphrase_api'
urlpatterns = [
    path('', include(router.urls)),
]
