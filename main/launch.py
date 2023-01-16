from main.models import Route, Station, MistakesRoute, MistakesStation
from django.utils.timezone import utc
import datetime



class Launch:
    def __init__(self):
        self.launched = False
        self.routes = []
        self.stations = []
        self.row_data_lines_count = 0
        self.stop_point = 0
        self.launched = False

    def launch_stations(self):
        row_data = []

        with open('Helsingin_ja_Espoon_kaupunkipy%C3%B6r%C3%A4asemat_avoin.csv', 'r', encoding='utf-8') \
                as stations_file:
            i: int
            i = 0
            for line in stations_file:

                if i != 0:
                    row_data.append(line)
                i = i + 1
        self.row_data_lines_count = self.row_data_lines_count+len(row_data)

        for j in range(0, len(row_data)):
            data = []
            if '"' not in row_data[j]:
                data = row_data[j].split(',')

            elif '"' in row_data[j]:
                data = []
                all_info = row_data[j]
                counter = 0
                re_write = ''
                for k in range(0, len(all_info)):
                    letter = all_info[k]
                    if '"' in all_info[k]:
                        counter = counter + 1
                    if counter % 2 != 0:
                        if ',' in all_info[k]:
                            letter = '&comma;'

                    re_write = re_write + letter

                data = re_write.split(',')
                for numb in range(0, len(data)):
                    if '&comma;' in data[numb]:
                        data[numb] = data[numb].replace('&comma;', ',')
            try:
                station = Station()
                station.f_id = data[0]
                station.station_id = data[1]
                station.name_fin = data[2]
                station.name_swd = data[3]
                station.name_eng = data[4]
                station.address_fin = data[5]
                station.address_swd = data[6]
                station.city_fin = data[7]
                station.city_swd = data[8]
                station.operator = data[9]
                station.capacity = data[10]
                station.coord_x = data[11]
                station.coord_y = data[12]

                self.stations.append(station)
                station.save()

            except:
                mistake = MistakesStation()
                mistake.mistake_station_id = j
                mistake.info_line = row_data[j]
                mistake.save()

        return self.stations

    def launch_routes(self):
        row_data = []
        with open('2021-05.csv', 'r', encoding='utf-8') as route_file1:
            i: int
            i = 0
            for line in route_file1:
                if i != 0:
                    row_data.append(line)
                i = i + 1
                if i % 10000 == 0:
                    print(i)

        with open('2021-06.csv', 'r', encoding='utf-8') as route_file2:
            i: int
            i = 0
            for line in route_file2:

                if i != 0:
                    row_data.append(line)
                i = i + 1
                if i % 100000 == 0:
                    print(i)

        with open('2021-07.csv', 'r', encoding='utf-8') as route_file2:
            i: int
            i = 0
            for line in route_file2:

                if i != 0:
                    row_data.append(line)
                i = i + 1
                if i % 100000 == 0:
                    print(i)
        self.row_data_lines_count = self.row_data_lines_count + len(row_data)

        if self.stop_point == 0:
            n = 0
        else:
            n = self.stop_point+1
            already = len(Route.objects.all())
            mistakes = len(MistakesRoute.objects.all)
            print("checkout_point: mistakes ", mistakes, 'already in base', already, ' lines readed', n-1)
            print('How many already in the base:', len(already))

        for j in range(n, len(row_data)):
            data = []

            if '"' not in row_data[j]:
                data = row_data[j].split(',')

            elif '"' in row_data[j]:

                data = []
                all_info = row_data[j]
                counter = 0
                re_write = ''
                for k in range(0, len(all_info)):
                    letter = all_info[k]
                    if '"' in all_info[k]:
                        counter = counter + 1
                    if counter % 2 != 0:
                        if ',' in all_info[k]:
                            letter = '&comma;'

                    re_write = re_write + letter

                data = re_write.split(',')

                for numb in range(0, len(data)):
                    if '&comma' in data[numb]:
                        data[numb] = data[numb].replace('&comma;', ',')
            try:
                if float(data[6]) >= 10.00 and float(data[7]) >= 10.00:
                    route = Route()
                    route.route_id = j
                    departure_time = data[0].split('T')
                    date_dep = departure_time[0].split('-')
                    year = int(date_dep[0])
                    month = int(date_dep[1])
                    day = int(date_dep[1])
                    time_dep = departure_time[1].split(':')
                    hour = int(time_dep[0])
                    minute = int(time_dep[1])
                    second = int(time_dep[2])
                    dept_time = datetime.datetime(year, month, day, hour, minute, second).replace(tzinfo=utc)
                    route.departure_time = dept_time
                    return_time = data[1].split('T')
                    date_ret = return_time[0].split('-')
                    year1 = int(date_ret[0])
                    month1 = int(date_ret[1])
                    day1 = int(date_ret[1])
                    time_dep1 = return_time[1].split(':')
                    hour1 = int(time_dep1[0])
                    minute1 = int(time_dep1[1])
                    second1 = int(time_dep1[2])
                    ret_time = datetime.datetime(year1, month1, day1, hour1, minute1, second1).replace(tzinfo=utc)
                    route.return_time = ret_time
                    route.departure_station_id = data[2]
                    route.departure_station_name = data[3]
                    route.return_station_id = data[4]
                    route.return_station_name = data[5]
                    route.covered_distance = data[6]
                    route.duration = data[7]
                    route.save()

            except:
                mistake = MistakesRoute()
                mistake.mistake_route_id = j
                mistake.info_line = row_data[j]
                mistake.save()

                print("Mistakes found in data: ", j)
                print(row_data[j])

            if j % 1000 == 0:
                print(j)
        self.stop_point = j
        print(self.stop_point)

        return self.routes

    # function for checking correctness of database populating process and consistency of information taken from the
    # given csv-files and placed in database
    def check_launch(self):
        row_data = []
        missed = []
        count = 0
        counter_viallinen = 0
        with open('2021-05.csv', 'r', encoding='utf-8') as route_file1:
            i: int
            i = 0
            for line in route_file1:
                if i != 0:
                    row_data.append(line)
                i = i + 1

        with open('2021-06.csv', 'r', encoding='utf-8') as route_file2:
            i: int
            i = 0
            for line in route_file2:

                if i != 0:
                    row_data.append(line)
                i = i + 1

        with open('2021-07.csv', 'r', encoding='utf-8') as route_file3:
            i: int
            i = 0
            for line in route_file3:

                if i != 0:
                    row_data.append(line)
                i = i + 1
        count = 0
        print(' Length of the array after reading file: '+str(len(row_data)))
        for j in range(0, len(row_data)):
            data = []

            if '"' not in row_data[j]:
                data = row_data[j].split(',')

            elif '"' in row_data[j]:
                data = []
                all_info = row_data[j]
                counter = 0
                re_write = ''
                for k in range(0, len(all_info)):
                    letter = all_info[k]
                    if '"' in all_info[k]:
                        counter = counter + 1
                    if counter % 2 != 0:
                        if ',' in all_info[k]:
                            letter = '&comma;'

                    re_write = re_write + letter

                data = re_write.split(',')

                for numb in range(0, len(data)):
                    if '&comma' in data[numb]:
                        data[numb] = data[numb].replace('&comma;', ',')

            try:
                if float(data[6]) < 10.00 or float(data[7]) < 10.00:
                    missed.append(row_data[j])

                elif float(data[6]) >= 10.00 and float(data[7]) >= 10.00:
                    route = Route()
                    route.route_id = j
                    departure_time = data[0].split('T')
                    date_dep = departure_time[0].split('-')
                    year = int(date_dep[0])
                    month = int(date_dep[1])
                    day = int(date_dep[1])
                    time_dep = departure_time[1].split(':')
                    hour = int(time_dep[0])
                    minute = int(time_dep[1])
                    second = int(time_dep[2])
                    dept_time = datetime.datetime(year, month, day, hour, minute, second).replace(tzinfo=utc)
                    route.departure_time = dept_time
                    return_time = data[1].split('T')
                    date_ret = return_time[0].split('-')
                    year1 = int(date_ret[0])
                    month1 = int(date_ret[1])
                    day1 = int(date_ret[1])
                    time_dep1 = return_time[1].split(':')
                    hour1 = int(time_dep1[0])
                    minute1 = int(time_dep1[1])
                    second1 = int(time_dep1[2])
                    ret_time = datetime.datetime(year1, month1, day1, hour1, minute1, second1).replace(tzinfo=utc)
                    route.return_time = ret_time
                    route.departure_station_id = data[2]
                    route.departure_station_name = data[3]
                    route.return_station_id = data[4]
                    route.return_station_name = data[5]
                    route.covered_distance = data[6]
                    route.duration = data[7]
            except:
                counter_viallinen = counter_viallinen+1

        number_of_routes = Route.objects.all().count()
        number_of_invalid = MistakesRoute.objects.all().count()
        sum_info = number_of_routes + number_of_invalid + len(missed)
        mistakes_in_data = MistakesRoute.objects.all().count()

        if (20 > len(row_data) - sum_info >= 0) or (-20 < len(row_data) - sum_info <= 0) and \
                counter_viallinen == mistakes_in_data:
            self.launched = True

        return self.launched





