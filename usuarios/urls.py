from django.urls import path
from .views import *

app_name = 'usuarios'

urlpatterns = [
    path('', Login.as_view(),)
]
