from django.urls import path
from . import views

urlpatterns = [

    # url and function for main page
    path('', views.index, name='index'),
    path('stations/', views.stations, name='stations'),
    path('routes/', views.routes, name='routes'),
    path('show_station/<station_id>', views.show_station, name='show_station'),
    path('show_station/<station_id>/<month>/', views.show_station_per_month, name='show_station_per_month'),
    path('show_route/<route_id>', views.show_route, name='show_route'),



    ]
