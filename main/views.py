from django.shortcuts import render, redirect
from .launch import Launch
from .models import Station, Route
from django.core.paginator import Paginator
from django.db.models import Q, Avg
from django.db import connection
from .forms import StationForm, FiltersForm, UpdateStationForm, RouteForm, UpdateRouteForm
from django.contrib import messages
from .useradmin import UserStatus
import calendar
import datetime


def index(request):
    #error_message = 'Success!!!!'
    # this is special launch class object which is needed in information from given files is not in database.
    # Notice that process off populating empty database can take long time.
    # if database is already populated with info, please do not uncomment following 7 row under the comment sign,
    # so this code do not  interrupt normal functionality of this app
    #launch = Launch()
    # if Station.objects.count() < 1:
    #    launch = Launch()
    #launch.launch_stations()
    # if Route.objects.count() < 1:
    #launch.launch_routes()
    #success = launch.check_launch()
    #if not success:
    #    error_message = 'There is no full consistency in information in database'

    # this function converts seconds and meters into min and km, and add info to additional columns to database
    # launch.change_measurements()

    # this is the end of part of the code, which is needed for populating empty database

    station_number = Station.objects.all().count()
    routes_number = Route.objects.all().count()

    session = request.session
    status = UserStatus(request)
    user_status = session.get('status')

    with connection.cursor() as cursor:
        cursor.execute("SELECT MAX(duration_min) FROM main_route")
        rows = cursor.fetchone()
    longest_route_duration = rows[0]

    with connection.cursor() as cursor:
        cursor.execute("SELECT MAX(covered_distance_km) FROM main_route")
        rows1 = cursor.fetchone()
    longest_route_distance = rows1[0]

    with connection.cursor() as cursor:
        cursor.execute("SELECT MIN(duration_min) FROM main_route")
        rows = cursor.fetchone()
    min_route_duration = rows[0]

    with connection.cursor() as cursor:
        cursor.execute("SELECT MIN(covered_distance_km) FROM main_route")
        rows1 = cursor.fetchone()
    min_route_distance = rows1[0]

    with connection.cursor() as cursor:
        cursor.execute('SELECT departure_station_id_id FROM (SELECT departure_station_id_id, '
                       'COUNT(departure_station_id_id) AS RETURN_COUNT FROM main_route '
                       'GROUP BY departure_station_id_id) '
                       'ORDER BY RETURN_COUNT DESC', )
        rows4 = cursor.fetchall()

        most_popular_station = Station.objects.get(station_id=rows4[0][0])

    with connection.cursor() as cursor:
        cursor.execute('SELECT departure_station_id_id FROM (SELECT departure_station_id_id, '
                       'COUNT(departure_station_id_id) AS RETURN_COUNT FROM main_route '
                       'GROUP BY departure_station_id_id) '
                       'ORDER BY RETURN_COUNT', )
        rows5 = cursor.fetchall()
        for el in rows5:

            if '999' not in el and '997' not in el:
                stat = el[0]
                break

            else:
                pass

        least_popular_station = Station.objects.get(station_id=stat)

    return render(request, 'index.html', {  # 'error_message': error_message,
                                           'status': user_status,
                                           'stations': station_number, 'routes_total': routes_number,
                                           'duration_max': longest_route_duration,
                                           'distance_max': longest_route_distance,
                                           'duration_min': min_route_duration,
                                           'distance_min': min_route_distance,
                                           'most_popular': most_popular_station,
                                           'least_popular': least_popular_station
                                          })


def change_status(request, stat):

    request.session['status'] = stat

    return redirect('index')


def stations(request):

    user_status = request.session['status']
    stations_all = Station.objects.all()
    pagination = Paginator(Station.objects.all(), 50)
    page = request.GET.get('page')
    station_on_page = pagination.get_page(page)

    return render(request, 'stations.html', {'status': user_status, 'stations': stations_all,
                                             'station_on_page': station_on_page})


def stations_sorted(request, column, order):

    user_status = request.session['status']

    if 'desc' in order:
        col = "-" + column
        pagination = Paginator(Station.objects.order_by(col), 50)
        page = request.GET.get('page')
        station_on_page = pagination.get_page(page)
    else:

        pagination = Paginator(Station.objects.order_by(column), 50)
        page = request.GET.get('page')
        station_on_page = pagination.get_page(page)

    return render(request, 'stations.html', {'status': user_status, 'station_on_page': station_on_page})


def show_station(request, station_id):

    user_status = request.session['status']
    station_id = station_id
    station = Station.objects.get(station_id=station_id)
    info = {}
    try:
        avg_start = Route.objects.filter(departure_station_id_id=station_id).aggregate(Avg('covered_distance_km'))
        avg_start = avg_start['covered_distance_km__avg']
        avg_start = f"{avg_start:.2f}"
        avg_end = Route.objects.filter(return_station_id_id=station_id).aggregate(Avg('covered_distance_km'))
        avg_end = avg_end['covered_distance_km__avg']
        avg_end = f"{avg_end:.2f}"
        info['average_depart'] = avg_start
        info['average_ret'] = avg_end
        trip_from = Route.objects.filter(departure_station_id_id=station_id).count()
        trip_to = Route.objects.filter(return_station_id_id=station_id).count()
        info['trip_from'] = trip_from
        info['trip_to'] = trip_to

        with connection.cursor() as cursor:
            cursor.execute('SELECT return_station_id_id FROM (SELECT return_station_id_id, '
                           'COUNT(return_station_id_id) AS RETURN_COUNT FROM main_route '
                           'WHERE departure_station_id_id=%s GROUP BY return_station_id_id) '
                           'ORDER BY RETURN_COUNT DESC', (station_id, ))
            rows = cursor.fetchall()
        from_station = []
        p = 0
        for el in rows:
            if p < 5:
                station2 = Station.objects.get(pk=el[0])
                from_station.append(station2)
                p = p + 1
            else:
                break

        with connection.cursor() as cursor:
            cursor.execute(
                'SELECT departure_station_id_id FROM (SELECT departure_station_id_id, '
                'COUNT(departure_station_id_id) AS DEPART_COUNT FROM main_route '
                'WHERE return_station_id_id=%s GROUP BY departure_station_id_id) '
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
        return render(request, 'show_station.html', {'status': user_status,'station': station, 'info': info,
                                                     'from_station': from_station,
                                                     'to_station': to_station})
    except:
        mistake = 'There are no information about routes at this station'
        return render(request, 'show_station.html', {'status': user_status, 'station': station,
                                                     'mistake': mistake})


def show_station_per_month(request, station_id, month):

    user_status = request.session['status']
    year = '2021'
    month_number = int(month)
    month_name = calendar.month_name[month_number]
    station = Station.objects.get(station_id=station_id)
    info = {}

    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT AVG(covered_distance) FROM main_route WHERE (departure_station_id_id=%s "
            "AND strftime('%%m', departure_time)=%s "
            "AND strftime('%%Y', departure_time)=%s)", (station_id, str(month), year))
        rows = cursor.fetchall()

    avg_start = rows[0][0]
    avg_start = f"{avg_start:.2f}"

    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT AVG(covered_distance) FROM main_route WHERE (return_station_id_id=%s "
            "AND strftime('%%m', departure_time)=%s "
            "AND strftime('%%Y', departure_time)=%s)", (station_id, str(month), year))
        rows2 = cursor.fetchall()

    avg_end = rows2[0][0]

    avg_end = f"{avg_end:.2f}"

    info['average_depart'] = avg_start
    info['average_ret'] = avg_end

    with connection.cursor() as cursor:
        cursor.execute(
            'SELECT return_station_id_id FROM (SELECT return_station_id_id, '
            'COUNT(return_station_id_id) AS RETURN_COUNT FROM main_route '
            'WHERE (departure_station_id_id=%s AND strftime("%%m", departure_time)=%s '
            'AND strftime("%%Y", departure_time)=%s) GROUP BY return_station_id_id) '
            'ORDER BY RETURN_COUNT DESC', (station_id, str(month), year))
        rows_from = cursor.fetchall()
    from_station = []
    p = 0
    for el in rows_from:
        if p < 5:
            station2 = Station.objects.get(pk=el[0])
            from_station.append(station2)
            p = p + 1
        else:
            break

    with connection.cursor() as cursor:
        cursor.execute(
            'SELECT departure_station_id_id FROM (SELECT departure_station_id_id, '
            'COUNT(departure_station_id_id) AS DEPART_COUNT FROM main_route '
            'WHERE return_station_id_id=%s AND strftime("%%m", departure_time)=%s '
            'AND strftime("%%Y", departure_time)=%s '
            'GROUP BY departure_station_id_id) '
            'ORDER BY DEPART_COUNT DESC',
            (station_id, str(month), year))
        rows_start = cursor.fetchall()
    to_station = []
    n = 0
    for elem in rows_start:
        if n < 5:
            print(elem)
            station1 = Station.objects.get(pk=elem[0])
            to_station.append(station1)
            n = n + 1
        else:
            break

    with connection.cursor() as cursor:
        cursor.execute(
            'SELECT COUNT(route_id)  FROM main_route '
            'WHERE departure_station_id_id=%s AND strftime("%%m", departure_time)=%s '
            'AND strftime("%%Y", departure_time)=%s',
            (station_id, str(month), year))
        trip_from = cursor.fetchall()
    trip_from = trip_from[0][0]

    info['trip_from'] = trip_from
    with connection.cursor() as cursor:
        cursor.execute(
            'SELECT COUNT(route_id)  FROM main_route '
            'WHERE return_station_id_id=%s AND strftime("%%m", departure_time)=%s '
            'AND strftime("%%Y", departure_time)=%s',
            (station_id, str(month), year))
        trip_to = cursor.fetchall()
    trip_to = trip_to[0][0]

    info['trip_from'] = trip_from
    info['trip_to'] = trip_to

    return render(request, 'show_station_per_month.html', {'status': user_status, 'station': station,
                                                           'month': month, 'month_name': month_name,
                                                           'info': info, 'from_station': from_station,
                                                           'to_station': to_station})


def routes(request):

    user_status = request.session['status']
    if request.method == 'POST':
        form = FiltersForm(request.POST)
        departure_station_id = -1
        return_station_id = -1
        departure_station = -1
        return_station = -1
        distance = -1
        duration = -1
        start = -1
        end = -1
        if request.method == 'POST':
            if 'dep_st_id' in request.POST and form.data['dep_st_id'] not in '':
                departure_station_id = form.data['dep_st_id']

            if 'ret_st_id' in request.POST and form.data['ret_st_id'] not in '':
                return_station_id = form.data['ret_st_id']

            if 'dep_st_name' in request.POST and form.data['dep_st_name'] not in '':
                departure_station = form.data['dep_st_name']

            if 'ret_st_name' in request.POST and form.data['ret_st_name'] not in '':
                return_station = form.data['ret_st_name']

            if 'distance' in request.POST and form.data['distance'] not in '':
                distance = form.data['distance']

            if 'duration' in request.POST and form.data['duration'] not in '':

                duration = form.data['duration']

            if 'date_start' in request.POST and form.data['date_start'] not in '':

                row = form.data['date_start'].split(' ')
                data_date = row[0].split('/')
                data_time = row[1].split(':')
                if data_date[0][0] == "0":
                    data_date[0] = data_date[0][1]
                date = datetime.datetime(int(data_date[2].strip()), int(data_date[1].strip()),
                                         int(data_date[0].strip()),
                                         int(data_time[0].strip()), int(data_time[1].strip()), 00)

                start = date

            if 'date_end' in request.POST and form.data['date_end'] not in '':

                row_end = form.data['date_end'].split(' ')
                data_date1 = row_end[0].split('/')
                data_time1 = row_end[1].split(':')
                if data_date1[0][0] == "0":
                    data_date1[0] = data_date1[0][1]
                date = datetime.datetime(int(data_date1[2].strip()), int(data_date1[1].strip()),
                                         int(data_date1[0].strip()),
                                         int(data_time1[0].strip()), int(data_time1[1].strip()), 00)
                end = date
                print('form return end', end)

        return redirect('routes_filter', departure_station_id, return_station_id, departure_station,
                        return_station, distance, duration, start, end)
    else:
        form = FiltersForm

    routes_all = Route.objects.all()
    pagination = Paginator(Route.objects.all(), 100)
    page = request.GET.get('page')
    route_on_page = pagination.get_page(page)

    return render(request, 'routes.html',  {'status': user_status, 'form': form, 'routes': routes_all,
                                            'route_on_page': route_on_page})


def routes_filter(request, dep_id, ret_id, dep, ret, distance, duration, start, end):

    user_status = request.session['status']
    departure_station_id = dep_id
    return_station_id = ret_id
    dep_st = dep
    ret_st = ret
    dist = distance
    dur = duration
    start = start
    end = end
    if '-1' in departure_station_id and '-1' in return_station_id and dep_st in '-1' and ret_st in '-1' \
            and dist in '-1' and dur in '-1' and start in '-1' and end in '-1':
        return redirect('routes')

    else:
        ask_string = "SELECT route_id FROM main_route WHERE "
        pieces = {}
        variables = ()
        if '-1' not in departure_station_id:
            piece = 'departure_station_id_id == %s'
            pieces['departure_station_id'] = piece
            variables = variables+(departure_station_id,)

        if '-1' not in return_station_id:
            piece = 'return_station_id_id == %s'
            pieces['return_station_id'] = piece

            variables = variables+(return_station_id,)
        if dep_st not in '-1':
            dep_st = dep_st+'%'
            piece = 'departure_station_name LIKE %s '
            pieces['departure_station_name'] = piece
            variables = variables + (dep_st,)
        if ret_st not in '-1':
            ret_st = ret_st + '%'
            piece = 'return_station_name LIKE %s'
            pieces['return_station_name'] = piece
            variables = variables + (ret_st,)
        if dist not in '-1':
            if '>' not in dist:
                boundaries = dist.split('-')

                piece = '(covered_distance_km >= %s AND covered_distance_km <= %s)'
                pieces['distance'] = piece
                variables = variables + (float(boundaries[0]), float(boundaries[1]),)
            elif '>' in dist:
                piece = 'covered_distance_km >= %s'
                pieces['distance'] = piece
                print(float(dist[1:len(dist)]))
                variables = variables + (float(dist[1:len(dist)]),)
        if dur not in '-1':
            if '>' not in dur:
                boundaries1 = dur.split('-')
                piece = '(duration_min >= %s AND duration_min <= %s)'
                pieces['duration'] = piece
                variables = variables + (float(boundaries1[0]), float(boundaries1[1]),)
            elif '>' in dur:
                piece = 'duration_min >= %s'
                pieces['duration'] = piece
                variables = variables + (float(dur[1:len(dur)]),)
        if start not in '-1' and end not in '-1':
            piece = '(departure_time >= %s AND departure_time <= %s)'
            variables = variables + (start, end, )
            pieces['departure_time'] = piece

        elif start not in '-1' and end in '-1':
            piece = 'departure_time >= %s'
            pieces['departure_time'] = piece
            variables = variables + (start,)

        elif end not in '-1' and start in '-1':
            piece = 'departure_time <= %%s%'
            pieces['departure_time'] = piece
            variables = variables + (end,)

        counter = 0

        for key, value in pieces.items():
            if counter == 0:
                ask_string = ask_string + value
                counter = counter+1
            else:
                ask_string = ask_string + ' AND ' + value

        print(ask_string)
        print(variables)
        with connection.cursor() as cursor:
            cursor.execute(
                ask_string,
                variables)
            rows_filter = cursor.fetchall()

        routes1 = []
        for el in rows_filter:
            route = Route.objects.get(route_id=el[0])
            routes1.append(route)

        result = len(routes1)
    if request.method == 'POST':

        form = FiltersForm(request.POST)

        departure_station_id = -1
        return_station_id = -1
        departure_station = -1
        return_station = -1
        distance = -1
        duration = -1
        start = -1
        end = -1
        if request.method == 'POST':
            if 'dep_st_id' in request.POST and form.data['dep_st_id'] not in '':
                departure_station_id = form.data['dep_st_id']

            if 'ret_st_id' in request.POST and form.data['ret_st_id'] not in '':
                return_station_id = form.data['ret_st_id']

            if 'dep_st_name' in request.POST and form.data['dep_st_name'] not in '':
                departure_station = form.data['dep_st_name']

            if 'ret_st_name' in request.POST and form.data['ret_st_name'] not in '':
                return_station = form.data['ret_st_name']

            if 'distance' in request.POST and form.data['distance'] not in '':
                distance = form.data['distance']

            if 'duration' in request.POST and form.data['duration'] not in '':
                duration = form.data['duration']

            if 'date_start' in request.POST and form.data['date_start'] not in '':
                print(form.data['date_start'])

                row = form.data['date_start'].split(' ')
                data_date = row[0].split('/')
                data_time = row[1].split(':')
                if data_date[0][0] == "0":
                    data_date[0] = data_date[0][1]
                date = datetime.datetime(int(data_date[2].strip()), int(data_date[1].strip()),
                                         int(data_date[0].strip()),
                                         int(data_time[0].strip()), int(data_time[1].strip()), 00)

                start = date
                print('form return start', start)

            if 'date_end' in request.POST and form.data['date_end'] not in '':
                print(form.data['date_end'])
                row_end = form.data['date_end'].split(' ')
                data_date1 = row_end[0].split('/')
                data_time1 = row_end[1].split(':')
                if data_date1[0][0] == "0":
                    data_date1[0] = data_date1[0][1]
                date = datetime.datetime(int(data_date1[2].strip()), int(data_date1[1].strip()),
                                         int(data_date1[0].strip()),
                                         int(data_time1[0].strip()), int(data_time1[1].strip()), 00)
                end = date
                print('form return end', end)

            return redirect('routes_filter', departure_station_id, return_station_id, departure_station,
                            return_station, distance, duration, start, end)

    else:
        form = FiltersForm

    pagination = Paginator(routes1, 50)
    page = request.GET.get('page')
    route_on_page = pagination.get_page(page)
    return render(request, 'routes.html', {'status': user_status,
                                           'result': result, 'form': form, 'route_on_page': route_on_page})


def routes_sorted(request, column, order):

    user_status = request.session['status']
    if request.method == 'POST':
        form = FiltersForm(request.POST)
        departure_station_id = -1
        return_station_id = -1
        departure_station = -1
        return_station = -1
        distance = -1
        duration = -1
        start = -1
        end = -1
        if request.method == 'POST':
            if 'dep_st_id' in request.POST and form.data['dep_st_id'] not in '':
                departure_station_id = form.data['dep_st_id']

            if 'ret_st_id' in request.POST and form.data['ret_st_id'] not in '':
                return_station_id = form.data['ret_st_id']

            if 'dep_st_name' in request.POST and form.data['dep_st_name'] not in '':
                departure_station = form.data['dep_st_name']

            if 'ret_st_name' in request.POST and form.data['ret_st_name'] not in '':
                return_station = form.data['ret_st_name']

            if 'distance' in request.POST and form.data['distance'] not in '':
                distance = form.data['distance']

            if 'duration' in request.POST and form.data['duration'] not in '':
                duration = form.data['duration']

            if 'date_start' in request.POST and form.data['date_start'] not in '':
                print(form.data['date_start'])

                row = form.data['date_start'].split(' ')
                data_date = row[0].split('/')
                data_time = row[1].split(':')
                if data_date[0][0] == "0":
                    data_date[0] = data_date[0][1]
                date = datetime.datetime(int(data_date[2].strip()), int(data_date[1].strip()),
                                         int(data_date[0].strip()),
                                         int(data_time[0].strip()), int(data_time[1].strip()), 00)

                start = date
                print('form return start', start)

            if 'date_end' in request.POST and form.data['date_end'] not in '':
                print(form.data['date_end'])
                row_end = form.data['date_end'].split(' ')
                data_date1 = row_end[0].split('/')
                data_time1 = row_end[1].split(':')
                if data_date1[0][0] == "0":
                    data_date1[0] = data_date1[0][1]
                date = datetime.datetime(int(data_date1[2].strip()), int(data_date1[1].strip()),
                                         int(data_date1[0].strip()),
                                         int(data_time1[0].strip()), int(data_time1[1].strip()), 00)
                end = date
                print('form return end', end)

        return redirect('routes_filter', departure_station_id, return_station_id, departure_station,
                        return_station, distance, duration, start, end)

    else:
        form = FiltersForm

    if 'desc' in order:
        col = "-" + column
        pagination = Paginator(Route.objects.order_by(col), 50)
        page = request.GET.get('page')
        route_on_page = pagination.get_page(page)
    else:
        pagination = Paginator(Route.objects.order_by(column), 50)
        page = request.GET.get('page')
        route_on_page = pagination.get_page(page)

    return render(request, 'routes.html', {'status': user_status,  'form': form,
                                           'route_on_page': route_on_page})


def show_route(request, route_id):

    user_status = request.session['status']
    route_id = int(route_id)
    route = Route.objects.get(pk=route_id)
    dep_station = Station.objects.get(pk=route.departure_station_id_id)
    ret_station = Station.objects.get(pk=route.return_station_id_id)

    return render(request, 'show_route.html', {'status': user_status, 'route': route,
                                               'dep_station': dep_station, 'ret_station': ret_station})


def search_station(request):

    if request.method == 'POST':
        searched = request.POST['searched']
        if searched:
            return redirect('search_station_result', searched)
        else:
            return render(request, 'search_result_not_found.html')
    else:

        return render(request, 'search_result_not_found.html')


def search_station_result(request, searched):

    user_status = request.session['status']

    searched_stations = Station.objects.filter(Q(station_id__contains=searched) | Q(name_fin__contains=searched)
                                               | Q(name_swd__contains=searched) | Q(name_eng__contains=searched))

    pagination_st = Paginator(Station.objects.filter(Q(station_id__contains=searched)
                                                     | Q(name_fin__contains=searched)
                                                     | Q(name_swd__contains=searched)
                                                     | Q(name_eng__contains=searched)), 10)
    page_station = request.GET.get('page')
    stations_on_page = pagination_st.get_page(page_station)
    results_stations = len(searched_stations)
    print(searched, len(searched_stations))

    return render(request, 'search_stations_result.html', {'status': user_status, 'searched': searched,
                                                           'searched_stations': searched_stations,
                                                           'stations_on_page': stations_on_page,
                                                           'results_stations': results_stations,
                                                           })


def search_route(request):
    if request.method == 'POST':
        searched = request.POST['searched']

        return redirect('search_route_result', searched)
    else:

        return render(request, 'search_result_not_found.html')


def search_route_result(request, searched):

    user_status = request.session['status']

    searched_routes = Route.objects.filter(Q(route_id__contains=searched) |
                                           Q(departure_station_name__contains=searched) |
                                           Q(return_station_name__contains=searched)
                                           )

    pagination_route = Paginator(Route.objects.filter(Q(route_id__contains=searched) |
                                                      Q(departure_station_name__contains=searched) |
                                                      Q(return_station_name__contains=searched)
                                                      ), 50)
    page_route = request.GET.get('page')
    routes_on_page = pagination_route.get_page(page_route)

    results_routes = len(searched_routes)

    print(searched, len(searched_routes))

    return render(request, 'search_route_result.html', {'status': user_status, 'searched': searched,
                                                        'searched_routes': searched_routes,
                                                        'routes_on_page': routes_on_page,
                                                        'results_routes': results_routes
                                                        })


def add_station(request):

    user_status = request.session['status']

    if request.method == 'POST':
        form = StationForm(request.POST)
        if form.is_valid():
            new_station = form.save(commit=False)

            new_station.save()
            messages.success(request, 'Station ' + new_station.name_fin + ' was successfully added')
            return redirect('/stations')
    else:
        form = StationForm
        context = {

            'form': form,
            'status': user_status
        }

        return render(request, 'add_station.html', context)


def update_station(request, station_id):

    user_status = request.session['status']
    station_update = Station.objects.get(pk=station_id)
    form = UpdateStationForm(request.POST or None, instance=station_update)
    if form.is_valid():
        updated_station = form.save(commit=False)
        updated_station.f_id = station_update.f_id
        updated_station.station_id = station_update.station_id

        updated_station.save()

        return redirect('/stations')

    return render(request, 'update_station.html', {'status': user_status,
                                                   'station': station_update, 'form': form})


def delete_station(request, station_id):
    station = Station.objects.get(station_id=station_id)
    try:
        station.delete()
        messages.success(request, 'Station ' + station.name_fin + ' was successfully deleted')
        return redirect('/stations')

    except:
        messages.error(request, 'You can not delete Station if any route belong to it. '
                                'Delete all the routes connected with this station first')
        return redirect('/stations')


def add_route(request):

    user_status = request.session['status']
    if request.method == 'POST':
        form = RouteForm(request.POST)

        if form.is_valid():
            if len(str(form.data['route_id'])) > 7:
                route_update = Route()
                route_update.route_id = form.data['route_id'].strip()

                try:
                    dep_id = form.data['dep_st_id'].strip()
                    dep_station = Station.objects.get(pk=dep_id)
                    route_update.departure_station_id = dep_station
                except:
                    messages.success(request, 'Departure station id not found. Please add station first.')
                    return render(request, 'add_route.html', {'status': user_status,
                                                              'route': route_update, 'form': form,
                                                              'message': messages})

                try:
                    ret_id = form.data['ret_st_id'].strip()
                    ret_station = Station.objects.get(pk=ret_id)
                    route_update.return_station_id = ret_station
                except:
                    messages.success(request, 'Return station id not found. Please add station first.')
                    return render(request, 'add_route.html', {'status': user_status, 'route': route_update,
                                                              'form': form,
                                                              'message': messages})

                route_update.departure_station_name = form.data['dep_st_name'].strip()
                route_update.return_station_name = form.data['ret_st_name'].strip()

                route_update.duration = int(form.data['duration'].strip())
                route_update.duration_min = route_update.duration/60
                route_update.duration_min = f"{route_update.duration_min:.2f}"

                route_update.covered_distance = int(form.data['distance'].strip())
                route_update.covered_distance_km = route_update.covered_distance / 1000
                route_update.covered_distance_km = f"{route_update.covered_distance_km:.3f}"

                route_update.departure_time = form.data['date_start'].strip()
                row = form.data['date_start'].split(' ')
                data_date = row[0].split('/')
                data_time = row[1].split(':')
                if data_date[0][0] == "0":
                    data_date[0] = data_date[0][1]
                date = datetime.datetime(int(data_date[2].strip()), int(data_date[1].strip()),
                                         int(data_date[0].strip()),
                                         int(data_time[0].strip()), int(data_time[1].strip()), 00)

                route_update.departure_time = date

                row_end = form.data['date_end'].strip().split(' ')
                data_date1 = row_end[0].split('/')
                data_time1 = row_end[1].split(':')
                if data_date1[0][0] == "0":
                    data_date1[0] = data_date1[0][1]
                date1 = datetime.datetime(int(data_date1[2].strip()), int(data_date1[1].strip()),
                                          int(data_date1[0].strip()),
                                          int(data_time1[0].strip()), int(data_time1[1].strip()), 00)
                route_update.return_time = date1

                route_update.save()
                messages.success(request, 'Route ' + str(route_update.route_id) + ' was successfully added')
                return redirect('routes')
            else:
                form = RouteForm
                messages.success(request, 'Route id should be more than 4 000 000')

                return render(request, 'add_route.html', {

                    'form': form,
                    'message': messages,
                    'status': user_status
                })
        else:
            form = RouteForm
            messages.success(request, 'Route info is not valid')

            return render(request, 'add_route.html', {

                'form': form,
                'message': messages,
                'status': user_status
            })
    else:
        form = RouteForm

        return render(request, 'add_route.html', {

                'form': form,

                'status': user_status
            })


def update_route(request, route_id):

    user_status = request.session['status']
    route_update = Route.objects.get(pk=route_id)
    form = UpdateRouteForm()

    if request.method == 'POST':
        form = UpdateRouteForm(request.POST)

        if 'dep_st_id' in request.POST and form.data['dep_st_id'] != '':
            try:
                dep_station = Station.objects.get(pk=form.data['dep_st_id'].strip())
                route_update.departure_station_id = dep_station
            except:
                messages.success(request, 'Departure station id not found. Please add station first.')
                return render(request, 'update_route.html', {'status': user_status, 'route': route_update,
                                                             'form': form,
                                                             'message': messages})

        if 'ret_st_id' in request.POST and form.data['ret_st_id'] != '':
            try:
                ret_station = Station.objects.get(pk=form.data['ret_st_id'].strip())
                route_update.return_station_id = ret_station
            except:
                messages.success(request, 'Return station id not found. Please add station first.')
                return render(request, 'update_route.html', {'status': user_status, 'route': route_update,
                                                             'form': form,
                                                             'message': messages})

        if 'dep_st_name' in request.POST and form.data['dep_st_name'] != '':
            route_update.departure_station_name = form.data['dep_st_name'].strip()
        if 'ret_st_name' in request.POST and form.data['ret_st_name'] != '':
            route_update.return_station_name = form.data['ret_st_name'].strip()
        if 'duration' in request.POST and form.data['duration'] != '':
            route_update.duration = int(form.data['duration'].strip())
            route_update.duration_min = route_update.duration / 60
            route_update.duration_min = f"{route_update.duration_min:.2f}"
        if 'distance' in request.POST and form.data['distance'] != '':
            route_update.covered_distance = int(form.data['distance'].strip())
            route_update.covered_distance_km = route_update.covered_distance/1000
            route_update.covered_distance_km = f"{route_update.covered_distance_km:.3f}"

        if 'date_start' in request.POST and form.data['date_start'] != '':
            route_update.departure_time = form.data['date_start'].strip()
            row = form.data['date_start'].split(' ')
            data_date = row[0].split('/')
            data_time = row[1].split(':')
            if data_date[0][0] == "0":
                data_date[0] = data_date[0][1]
            date = datetime.datetime(int(data_date[2].strip()), int(data_date[1].strip()),
                                     int(data_date[0].strip()),
                                     int(data_time[0].strip()), int(data_time[1].strip()), 00)

            route_update.departure_time = date
        if 'date_end' in request.POST and form.data['date_end'] != '':
            route_update.return_time = form.data['date_end'].strip()
            row_end = form.data['date_end'].strip().split(' ')
            data_date1 = row_end[0].split('/')
            data_time1 = row_end[1].split(':')
            if data_date1[0][0] == "0":
                data_date1[0] = data_date1[0][1]
            date1 = datetime.datetime(int(data_date1[2].strip()), int(data_date1[1].strip()),
                                      int(data_date1[0].strip()),
                                      int(data_time1[0].strip()), int(data_time1[1].strip()), 00)
            route_update.return_time = date1

        try:
            route_update.save()
        except:
            print('NOT SAVED!!!!!!')

        return redirect('routes')

    return render(request, 'update_route.html', {'status': user_status, 'route': route_update, 'form': form})


def delete_route(request, route_id):

    if len(route_id) < 8:
        messages.error(request, 'You can not delete route from main routes (routes id under 4 000 000)')
        return redirect('/routes')
    else:
        route = Route.objects.get(route_id=route_id)
        route.delete()
        messages.success(request, 'Route ' + route.route_id + ' was successfully deleted')
        return redirect('/routes')
