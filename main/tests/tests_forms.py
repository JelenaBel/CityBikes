from django.test import TestCase
from main.forms import StationForm, FiltersForm
import datetime


class TestForms(TestCase):
    def test_StationForm_valid_data(self):
        form = StationForm(data={
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
            "coord_x": '435834543',
            "coord_y": '345435435'


        })
        self.assertTrue(form.is_valid())

    def test_StationForm_valid_no_data(self):

        form = StationForm(data={

        })
        self.assertFalse(form.is_valid())

    def test_StationFrom_no_id(self):

        form = StationForm(data={
            'f_id': 11,
            "name_fin": 'TEST',
            "name_swd": 'TEST',
            "name_eng": 'TEST',
            "address_fin": 'TEST',
            "address_swd": 'TEST',
            "city_fin": 'TEST',
            "city_swd": 'TEST',
            "operator": 'TEST',
            "capacity": 123,
            "coord_x": '435834543',
            "coord_y": '345435435'


        })
        self.assertFalse(form.is_valid())

    def test_StationFrom_no_coord(self):
        form = StationForm(data={
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

        self.assertFalse(form.is_valid())

    def test_FiltersForm_valid_data(self):
        data1 = datetime.datetime(2021, 11, 10, 12, 00, 00)
        data2 = datetime.datetime(2021, 11, 10, 13, 00, 00)
        form = FiltersForm(data={
            'dep_st_id': 11,
            'ret_st_id': 10567488,
            "dep_st_name": 'TEST',
            "ret_st_name": 'TEST',
            "distance": '10-20',
            "duration": '240-480',
            "date_start": data1,
            "date_end": data2


        })

        self.assertTrue(form.is_valid())
