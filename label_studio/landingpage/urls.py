from django.urls import path
from . import views

app_name = 'landingpage'

urlpatterns = [
    path('', views.landingpageopen, name= 'landingpageopen'),
]