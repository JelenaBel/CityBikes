from django.shortcuts import render
from .launch import Launch
from .models import Station, Route, MistakesRoute
from django.core.paginator import Paginator

# Create your views here.


def index(request):
    # this is special launch class object which is needed in information from given files is not in database.
    # Notice that process off populating empty database can take long time.
    # if database is already populated with info, please put following 7 row under the comment sign, so this code do not
    # interrupt normal functionality of this app
    launch = Launch()
    if Station.objects.count() < 1:
        launch = Launch()
        launch.launch_stations()
    if Route.objects.count() < 1:
        launch.launch_routes()
    success = launch.check_launch()
    if not success:
        error_message = 'There is no consistency in information in database'
    # this is the end of part of the code, which is needed for populating empty database

    #
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
    print(len(station_id))
    station_id = int(station_id)
    station = Station.objects.get(pk=station_id)
    info = {}
    routes_start = Route.objects.filter(departure_station_id=station_id)
    routes_ends = Route.objects.filter(return_station_id=station_id)
    address = station.address_fin + station.city_fin

    # counting average journey length stating from this station
    summa_dep = 0
    for k in range(0, len(routes_start)):

        summa_dep = summa_dep+float(routes_start[k].covered_distance)
    average_depart = summa_dep/len(routes_start)
    average_depart = f"{average_depart:.2f}"
    info['average_depart'] = average_depart

    # counting average journey length ending at this station
    summa_ret = 0
    for m in range(0, len(routes_ends)):

        summa_ret = summa_ret + float(routes_ends[m].covered_distance)
    average_ret = summa_dep / len(routes_ends)
    average_ret = f"{average_ret:.2f}"
    info['average_ret'] = average_ret

    # counting Top 5 most popular departure stations for journeys ending at the station
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
    print(return_stations)
    top_five_return = {}
    for ret_station in return_stations:
        appearance = return_stations.count(ret_station)
        if ret_station not in top_five_return.keys():
            top_five_return[ret_station] = appearance
    top_five_return = sorted(top_five_return.items(), key=lambda x: x[1], reverse=True)
    print(top_five_return)
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