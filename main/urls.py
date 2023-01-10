from django.urls import path
from . import views

urlpatterns = [

    # url and function for main page
    path('', views.index, name='index'),
    path('stations/', views.stations, name='stations'),
    path('routes/', views.routes, name='routes'),
    path('show_station/<station_id>', views.show_station, name='show_station'),



    ]
