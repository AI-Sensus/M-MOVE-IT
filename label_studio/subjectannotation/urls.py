from django.urls import path
from . import views

app_name = 'subjectannotation'

urlpatterns = [
    path('', views.annotationtaskpage, name= 'annotationtaskpage'),
    path('create/', views.createannotationtask, name='create'),
    path('export/<int:project_id>',views.exportannotations,name='export')
]
