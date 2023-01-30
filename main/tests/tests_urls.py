from django.test import SimpleTestCase
from django.urls import reverse, resolve
from main.views import index, stations, stations_sorted, show_station, show_station_per_month, routes, routes_filter
from main.views import routes_sorted, show_route, search_station, search_station_result, search_route
from main.views import search_route_result, add_station


class TestUrls(SimpleTestCase):
    # url and function for main page
    def test_main_url(self):
        url = reverse('index')
        print(resolve(url))
        self.assertEquals(resolve(url).func, index)

    # url and function for stations page
    def test_stations_url(self):
        url = reverse('stations')
        print(resolve(url))
        self.assertEquals(resolve(url).func, stations)

    # url and function for stations sorting result page
    def test_stations_sorted_url(self):
        url = reverse('stations_sorted', args=['station_id', 'desc'])
        print(resolve(url))
        self.assertEquals(resolve(url).func, stations_sorted)

    # url and function for show chosen stations page
    def test_show_station_url(self):
        url = reverse('show_station', args=['11'])
        print(resolve(url))
        self.assertEquals(resolve(url).func, show_station)

    # url and function for all routes page
    def test_routes_url(self):
        url = reverse('routes')
        print(resolve(url))
        self.assertEquals(resolve(url).func, routes)

    # url and function for show monthly statistic for chosen month for chosen station page
    def test_show_station_per_month_url(self):
        url = reverse('show_station_per_month', args=['11', '05'])
        print(resolve(url))
        self.assertEquals(resolve(url).func, show_station_per_month)

    # url and function for filtering routes and filtering results page
    def test_routes_filter_url(self):
        url = reverse('routes_filter', args=['1', '2', 'west', 'al', '0-1', '10-20', '-1', '-1'])
        print(resolve(url))
        self.assertEquals(resolve(url).func, routes_filter)

    # url and function sorting routes by column routes page
    def test_routes_sorted_url(self):
        url = reverse('routes_sorted', args=['duration_min', 'asc'])
        print(resolve(url))
        self.assertEquals(resolve(url).func, routes_sorted)

    # url and function for showing info for chosen route
    def test_show_route_url(self):
        url = reverse('show_route', args=['24798'])
        print(resolve(url))
        self.assertEquals(resolve(url).func, show_route)

    # function for searching stations
    def test_search_station_url(self):
        url = reverse('search_station')
        print(resolve(url))
        self.assertEquals(resolve(url).func, search_station)

    # url and function for searching result for stations
    def test_search_station_result_url(self):
        url = reverse('search_station_result', args=['center'])
        print(resolve(url))
        self.assertEquals(resolve(url).func, search_station_result)

    # function for searching routes
    def test_search_route_url(self):
        url = reverse('search_route')
        print(resolve(url))
        self.assertEquals(resolve(url).func, search_route)

    # url and function for searching result for routes
    def test_search_route_result_url(self):
        url = reverse('search_route_result', args=['center'])
        print(resolve(url))
        self.assertEquals(resolve(url).func, search_route_result)

    # url and function for adding new station
    def test_add_station_url(self):
        url = reverse('add_station')
        print(resolve(url))
        self.assertEquals(resolve(url).func, add_station)