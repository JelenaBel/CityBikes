from django.urls import path
from . import views

urlpatterns = [

    # url and function for main page
    path('', views.index, name='index'),
    path('stations/', views.stations, name='stations'),
    path('stations_sorted/<column>/<order>', views.stations_sorted, name="stations_sorted"),
    path('routes/', views.routes, name='routes'),
    path('routes_sorted/<column>/<order>', views.routes_sorted, name="routes_sorted"),
    path('routes_filter/<dep_id>/<ret_id>/<dep>/<ret>/<distance>/<duration>/<start>/<end>/', views.routes_filter,
         name="routes_filter"),
    path('show_station/<station_id>', views.show_station, name='show_station'),
    path('show_station/<station_id>/<month>/', views.show_station_per_month, name='show_station_per_month'),
    path('show_route/<route_id>', views.show_route, name='show_route'),
    path('search_station/', views.search_station, name='search_station'),
    path('search_station_result/<searched>', views.search_station_result, name='search_station_result'),
    path('search_route/', views.search_route, name='search_route'),
    path('search_route_result/<searched>', views.search_route_result, name='search_route_result'),
    path('add_station/', views.add_station, name="add_station"),
    path('update_station/<station_id>', views.update_station, name="update_station"),
    path('delete_station/<station_id>', views.delete_station, name="delete_station"),
    path('admin_stations/', views.admin_stations, name="admin_stations"),
    path('routes_admin/', views.routes_admin, name="routes_admin"),
    path('add_route/', views.add_route, name="add_route"),
    path('update_route/<route_id>', views.update_route, name="update_route"),
    path('delete_route/<route_id>', views.delete_route, name="delete_route"),
    path('change_status/<stat>', views.change_status, name="change_status"),

    ]
