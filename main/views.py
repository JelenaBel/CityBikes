from django.shortcuts import render
from .launch import Launch
from .models import Station, Route, MistakesRoute
from django.core.paginator import Paginator
from django.db.models import Sum, Q, Avg, Count

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
    print(station_id)

    station = Station.objects.get(pk=station_id)
    info = {}
    routes_start = Route.objects.filter(departure_station_id=station_id)
    avg_start = Route.objects.filter(departure_station_id=station_id).aggregate(Avg('covered_distance'))
    print('average start', avg_start)
    avg_start = avg_start['covered_distance__avg']
    avg_start = f"{avg_start:.2f}"

    routes_ends = Route.objects.filter(return_station_id=station_id)
    avg_end = Route.objects.filter(return_station_id=station_id).aggregate(Avg('covered_distance'))
    print('average end', avg_end)
    avg_end = avg_end['covered_distance__avg']
    avg_end = f"{avg_end:.2f}"
    info['average_depart'] = avg_start
    info['average_ret'] = avg_end

    # counting Top 5 most popular departure stations for journeys ending at the station
    routes_ends = Route.objects.filter(return_station_id=station_id)
    depart_stations = []
    for el_route in routes_ends:
        depart_stations.append(el_route.departure_station_id)

    top_five_depart = {}
    for dep_station in depart_stations:
        appearance = depart_stations.count(dep_station)
        if dep_station not in top_five_depart.keys():
            top_five_depart[dep_station] = appearance

    top_five_depart = sorted(top_five_depart.items(), key=lambda x: x[1], reverse=True)

    five_depart = []
    for m in range(0, 5):
        id_st = top_five_depart[m][0]
        dep_stat = Station.objects.get(pk=id_st)
        five_depart.append(dep_stat)

    # counting Top 5 most popular return stations for journeys starting from the station
    return_stations = []
    for el_route in routes_start:
        return_stations.append(el_route.return_station_id)

    top_five_return = {}
    for ret_station in return_stations:
        appearance = return_stations.count(ret_station)
        if ret_station not in top_five_return.keys():
            top_five_return[ret_station] = appearance
    top_five_return = sorted(top_five_return.items(), key=lambda x: x[1], reverse=True)

    five_ret = []

    for key_ret in range(0, 5):
        id_st = top_five_return[key_ret][0]
        ret_stat = Station.objects.get(pk=id_st)
        five_ret.append(ret_stat)

    return render(request, 'show_station.html', {'station': station, 'info': info, 'five_depart': five_depart,
                                                 'five_ret': five_ret})


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
