from django.urls import  path
from .import views
urlpatterns = [
    path('search_item', views.search_item, name='search_item'),
    path('search_item_sales', views.search_item_sales, name='search_item_sales'),
]