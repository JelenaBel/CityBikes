from django.shortcuts import render
from .launch import Launch
from .models import Station, Route, MistakesRoute
from django.core.paginator import Paginator
from django.db.models import Sum, Q, Avg, Count
import calendar
from calendar import HTMLCalendar
from django.db import connection

# Create your views here.


def index(request):
    # this is special launch class object which is needed in information from given files is not in database.
    # Notice that process off populating empty database can take long time.
    # if database is already populated with info, please do not uncomment following 7 row under the comment sign,
    # so this code do not  interrupt normal functionality of this app
    # launch = Launch()
    # if Station.objects.count() < 1:
    #    launch = Launch()
    #    launch.launch_stations()
    # if Route.objects.count() < 1:
    #    launch.launch_routes()
    # success = launch.check_launch()
    # if not success:
    #    error_message = 'There is no consistency in information in database'
    # this is the end of part of the code, which is needed for populating empty database

    station_number = Station.objects.all().count()
    routes_number = Route.objects.all().count()

    return render(request, 'index.html', {'stations': station_number, 'routes_total': routes_number})


def stations(request):
    stations = Station.objects.all()
    pagination = Paginator(Station.objects.all(), 50)
    page = request.GET.get('page')
    station_on_page = pagination.get_page(page)

    return render(request, 'stations.html', {'stations': stations, 'station_on_page': station_on_page})



def show_station(request, station_id):
    station = Station.objects.get(station_id=station_id)
    info = {}
    routes_start = Route.objects.filter(departure_station_id=station_id)
    avg_start = Route.objects.filter(departure_station_id=station_id).aggregate(Avg('covered_distance'))

    avg_start = avg_start['covered_distance__avg']
    avg_start = f"{avg_start:.2f}"

    routes_ends = Route.objects.filter(return_station_id=station_id)
    avg_end = Route.objects.filter(return_station_id=station_id).aggregate(Avg('covered_distance'))

    avg_end = avg_end['covered_distance__avg']
    avg_end = f"{avg_end:.2f}"
    info['average_depart'] = avg_start
    info['average_ret'] = avg_end

    with connection.cursor() as cursor:
        cursor.execute('SELECT return_station_id FROM (SELECT return_station_id, '
                       'COUNT(return_station_id) AS RETURN_COUNT FROM main_route '
                       'WHERE departure_station_id=%s GROUP BY return_station_id) '
                       'ORDER BY RETURN_COUNT DESC', (station_id, ))
        rows = cursor.fetchall()
    from_station = []
    p=0
    for el in rows:
        if p < 5:
            station2 = Station.objects.get(pk=el[0])
            from_station.append(station2)
            p=p+1
        else:
            break

    with connection.cursor() as cursor:
        cursor.execute(
            'SELECT departure_station_id FROM (SELECT departure_station_id, '
            'COUNT(departure_station_id) AS DEPART_COUNT FROM main_route '
            'WHERE return_station_id=%s GROUP BY departure_station_id) '
            'ORDER BY DEPART_COUNT DESC',
            (station_id,))
        rows = cursor.fetchall()
    to_station = []
    n = 0
    for elem in rows:
        if n < 5:
            print(elem)
            station1 = Station.objects.get(pk=elem[0])
            to_station.append(station1)
            n = n + 1
        else:
            break

    return render(request, 'show_station.html', {'station': station, 'info': info,  'from_station': from_station,
                                                 'to_station': to_station})


def show_station_per_month(request, station_id, month):
    year = 2021
    month_number=int(month)
    station = Station.objects.get(pk=station_id)

    info = {}
    avg_start = Route.objects.filter(
        departure_station_id=station_id,
        departure_time__month=month_number,
        departure_time__year=year
    ).aggregate(Avg('covered_distance'))

    print('Average start from this station', avg_start)
    avg_dep = Route.objects.filter(
        return_station_id=station_id,
        departure_time__month=month_number,
        departure_time__year=year
    ).aggregate(Avg('covered_distance'))

    print('Average return from this station', avg_dep)
    avg_start = avg_start['covered_distance__avg']
    avg_start = f"{avg_start:.2f}"
    avg_end = avg_dep['covered_distance__avg']
    avg_end = f"{avg_end:.2f}"

    info['average_depart'] = avg_start
    info['average_ret'] = avg_end
    return render(request, 'show_station_per_month.html', {'station': station, 'month': month, 'info': info })







def routes(request):
    routes = Route.objects.all()
    pagination = Paginator(Route.objects.all(), 100)
    page = request.GET.get('page')
    route_on_page = pagination.get_page(page)

    return render(request, 'routes.html', {'routes': routes, 'route_on_page': route_on_page})


def show_route(request, route_id):
    route_id = int(route_id)
    route = Route.objects.get(pk=route_id)
    dep_station = Station.objects.get(pk=route.departure_station_id)
    ret_station = Station.objects.get(pk=route.return_station_id)

    return render(request, 'show_route.html', {'route': route, 'dep_station': dep_station, 'ret_station': ret_station})
