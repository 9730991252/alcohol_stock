from django.urls import path
from . import views
urlpatterns = [
    path('owner_home/', views.owner_home, name='owner_home'),
    path('item/', views.item, name='item'),
    path('purchase/', views.purchase, name='purchase'),
    path('sales/', views.sales, name='sales'),
    path('report/', views.report, name='report'),
]