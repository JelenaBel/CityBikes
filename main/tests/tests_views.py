from django.test import TestCase, Client
from django.urls import reverse
from main.models import Station, Route
import datetime


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()

    def test_show_stations_GET(self):
        station1 = Station(
            f_id='1',
            station_id='1',
            name_fin='TEST',
            name_swd='TEST',
            name_eng='TEST',
            address_fin='TEST',
            address_swd='TEST',
            city_fin='TEST',
            city_swd='TEST',
            operator='TEST',
            capacity='23',
            coord_x='TEST',
            coord_y='TEST',
                )
        station1.save()
        route1 = Route(
            route_id='1',
            departure_time=datetime.datetime(2022, 11, 10, 12, 00, 00),
            return_time=datetime.datetime(2022, 11, 10, 13, 00, 00),
            departure_station_id=station1,
            departure_station_name='TEST',
            return_station_id=station1,
            return_station_name='TEST',
            covered_distance=3000,
            duration=3600,
            covered_distance_km=3,
            duration_min=60,
            )
        route1.save()

        show_station_url = reverse('show_station', args=[station1.station_id])

        response = self.client.get(show_station_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'show_station.html', )

    def test_show_route_GET(self):
        station1 = Station(
            f_id='1',
            station_id='1',
            name_fin='TEST',
            name_swd='TEST',
            name_eng='TEST',
            address_fin='TEST',
            address_swd='TEST',
            city_fin='TEST',
            city_swd='TEST',
            operator='TEST',
            capacity='23',
            coord_x='TEST',
            coord_y='TEST',
        )
        station1.save()
        route1 = Route(
            route_id='1',
            departure_time=datetime.datetime(2022, 11, 10, 12, 00, 00),
            return_time=datetime.datetime(2022, 11, 10, 13, 00, 00),
            departure_station_id=station1,
            departure_station_name='TEST',
            return_station_id=station1,
            return_station_name='TEST',
            covered_distance=3000,
            duration=3600,
            covered_distance_km=3,
            duration_min=60,
        )
        route1.save()

        show_route_url = reverse('show_route', args=[route1.route_id])

        response = self.client.get(show_route_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'show_route.html')

    def test_search_station_GET(self):
        station1 = Station(
            f_id='1',
            station_id='1',
            name_fin='TEST',
            name_swd='TEST',
            name_eng='TEST',
            address_fin='TEST',
            address_swd='TEST',
            city_fin='TEST',
            city_swd='TEST',
            operator='TEST',
            capacity='23',
            coord_x='TEST',
            coord_y='TEST',
        )
        station1.save()
        route1 = Route(
            route_id='1',
            departure_time=datetime.datetime(2022, 11, 10, 12, 00, 00),
            return_time=datetime.datetime(2022, 11, 10, 13, 00, 00),
            departure_station_id=station1,
            departure_station_name='TEST',
            return_station_id=station1,
            return_station_name='TEST',
            covered_distance=3000,
            duration=3600,
            covered_distance_km=3,
            duration_min=60,
        )
        route1.save()
        searched = 'TEST'

        show_route_url = reverse('search_station_result', args=[searched])

        response = self.client.get(show_route_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'search_stations_result.html')

    def test_search_route_GET(self):
        station1 = Station(
            f_id='1',
            station_id='1',
            name_fin='TEST',
            name_swd='TEST',
            name_eng='TEST',
            address_fin='TEST',
            address_swd='TEST',
            city_fin='TEST',
            city_swd='TEST',
            operator='TEST',
            capacity='23',
            coord_x='TEST',
            coord_y='TEST',
        )
        station1.save()
        route1 = Route(
            route_id=1,
            departure_time=datetime.datetime(2022, 11, 10, 12, 00, 00),
            return_time=datetime.datetime(2022, 11, 10, 13, 00, 00),
            departure_station_id=station1,
            departure_station_name='TEST',
            return_station_id=station1,
            return_station_name='TEST',
            covered_distance=3000,
            duration=3600,
            covered_distance_km=3,
            duration_min=60,
        )

        route1.save()
        searched = "TEST"

        search_route_result_url = reverse('search_route_result', args=[searched])
        response = self.client.get(search_route_result_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'search_route_result.html')

    def test_routes_filter_GET(self):
        station1 = Station(
            f_id='1',
            station_id='1',
            name_fin='TEST',
            name_swd='TEST',
            name_eng='TEST',
            address_fin='TEST',
            address_swd='TEST',
            city_fin='TEST',
            city_swd='TEST',
            operator='TEST',
            capacity='23',
            coord_x='TEST',
            coord_y='TEST',
        )
        station1.save()
        route1 = Route(
            route_id=1,
            departure_time=datetime.datetime(2022, 11, 10, 12, 00, 00),
            return_time=datetime.datetime(2022, 11, 10, 13, 00, 00),
            departure_station_id=station1,
            departure_station_name='TEST',
            return_station_id=station1,
            return_station_name='TEST',
            covered_distance=3000,
            duration=3600,
            covered_distance_km=3,
            duration_min=60,
        )

        route1.save()
        criteria = "TEST"

        routes_filter_url = reverse('routes_filter', args=[-1, criteria, -1, -1, '20-50', '120-240', -1, -1])
        response = self.client.get(routes_filter_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'routes.html')

    def test_show_station_per_month_GET(self):
        station1 = Station(
            f_id='1',
            station_id='1',
            name_fin='TEST',
            name_swd='TEST',
            name_eng='TEST',
            address_fin='TEST',
            address_swd='TEST',
            city_fin='TEST',
            city_swd='TEST',
            operator='TEST',
            capacity='23',
            coord_x='TEST',
            coord_y='TEST',
        )
        station1.save()
        route1 = Route(
            route_id='1',
            departure_time=datetime.datetime(2021, 11, 10, 12, 00, 00),
            return_time=datetime.datetime(2021, 11, 10, 13, 00, 00),
            departure_station_id=station1,
            departure_station_name='TEST',
            return_station_id=station1,
            return_station_name='TEST',
            covered_distance=3000,
            duration=3600,
            covered_distance_km=3,
            duration_min=60,
        )
        route1.save()
        station_id = 1

        show_station_per_month_url = reverse('show_station_per_month', args=[station_id, 11])

        response = self.client.get(show_station_per_month_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'show_station_per_month.html')

    def test_show_station_GET(self):
        station1 = Station(
            f_id='1',
            station_id='1',
            name_fin='TEST',
            name_swd='TEST',
            name_eng='TEST',
            address_fin='TEST',
            address_swd='TEST',
            city_fin='TEST',
            city_swd='TEST',
            operator='TEST',
            capacity='23',
            coord_x='TEST',
            coord_y='TEST',
        )
        station1.save()
        route1 = Route(
            route_id='1',
            departure_time=datetime.datetime(2021, 11, 10, 12, 00, 00),
            return_time=datetime.datetime(2021, 11, 10, 13, 00, 00),
            departure_station_id=station1,
            departure_station_name='TEST',
            return_station_id=station1,
            return_station_name='TEST',
            covered_distance=3000,
            duration=3600,
            covered_distance_km=3,
            duration_min=60,
        )
        route1.save()
        station_id = 1

        show_station_url = reverse('show_station', args=[station_id])

        response = self.client.get(show_station_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'show_station.html')

    def test_add_station_POST(self):
        add_station_url = reverse('add_station')

        response1 = self.client.post(add_station_url, {
            'f_id': 11,
            'station_id': 10567488,
            "name_fin": 'TEST',
            "name_swd": 'TEST',
            "name_eng": 'TEST',
            "address_fin": 'TEST',
            "address_swd": 'TEST',
            "city_fin": 'TEST',
            "city_swd": 'TEST',
            "operator": 'TEST',
            "capacity": 123,
        })
        station_id = 10567488
        show_station_url = reverse('show_station', args=[station_id])
        response2 = self.client.get(show_station_url)

        self.assertEqual(response1.status_code, 302)
        self.assertEqual(response2.status_code, 200)






