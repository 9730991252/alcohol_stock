from django.urls import path
from . import views

urlpatterns = [
    path('daly_report/', views.daly_report, name='daly_report'),

]
