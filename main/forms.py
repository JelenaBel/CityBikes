from .models import Station, Route
from django.forms import ModelForm, TextInput, Select,  CharField
from django import forms

DISTANCE_CHOICES = [('0-1', '0-1'), ('1-5', '1-5'), ('5-10', '5-10'), ('10-20', '10-20'), ('20-50', '20-50'),
                    ('50-100', '50-100'),  ('>100', '>100')]
DURATION_CHOICES = [('0-1', '0-1'), ('1-10', '1-10'), ('10-30', '10-30'), ('30-60', '30-60'),
                    ('60-120', '60-120'), ('120-240', '120-240'), ('>240', '>240')]


class StationForm(ModelForm):

    class Meta:
        model = Station
        fields = ['f_id', 'station_id', "name_fin", "name_swd", "name_eng", "address_fin",  "address_swd",
                  "city_fin", "city_swd", "operator", "capacity", "coord_x",
                  "coord_y"]

        widgets = {

            "f_id": TextInput(attrs={
                "label": "F ID",
                "class": "form-control form-control-sm",
                "placeholder": "f id"

            }),
            "station_id": TextInput(attrs={
                "label": "Station ID",
                "class": "form-control form-control-sm",
                "placeholder": "Station ID"

            }),
            "name_fin": TextInput(attrs={
                "label": "Name fin",
                "class": "form-control form-control-sm",
                "placeholder": "Station name (fin)"

            }),
            "name_swd": TextInput(attrs={

                "class": "form-control form-control-sm",
                "placeholder": "Station name (swd)"

            }),
            "name_eng": TextInput(attrs={

                "class": "form-control form-control-sm",
                "placeholder": "Station name (eng)"

            }),
            "address_fin": TextInput(attrs={

                "class": "form-control form-control-sm",
                "placeholder": "Address(fin)"

            }),
            "address_swd": TextInput(attrs={
                "label": "Station ID",
                "class": "form-control form-control-sm",
                "placeholder": "Address(swd)"

            }),
            'city_fin':  TextInput(attrs={

                "class": "form-control form-control-sm",
                "placeholder": "City (fin)"
            }),
            'city_swd': TextInput(attrs={

                "class": "form-control form-control-sm",
                "placeholder": "City (swd)"

            }),
            "operator": TextInput(attrs={
                "class": "form-control form-control-sm",
                "placeholder": "Operator"

            }),
            "capacity": TextInput(attrs={
                "class": "form-control form-control-sm",
                "placeholder": "Capacity"

            }),
            "coord_x": TextInput(attrs={
                "class": "form-control form-control-sm",
                "placeholder": "Longitude"

                }),

            "coord_y": TextInput(attrs={
                "class": "form-control form-control-sm",
                "placeholder": "Latitude"

            }),

        }


class FiltersForm(forms.Form):

        dep_st_id = forms.IntegerField(required=False

            )

        ret_st_id = forms.IntegerField(required=False


        )
        dep_st_name = forms.CharField(required=False

                                    )

        ret_st_name = forms.CharField(required=False

                                    )
        distance = forms.ChoiceField(
            required=False,
            widget=forms.RadioSelect(),
            choices=DISTANCE_CHOICES,

        )

        duration = forms.ChoiceField(
            required=False,
            widget=forms.RadioSelect(),
            choices=DURATION_CHOICES,

        )

        date_start = forms.DateTimeField(
            required=False,
            input_formats=['%d/%m/%Y %H:%M'],
            widget=forms.DateTimeInput(attrs={
                'onchange': 'form.submit();',
                'class': 'form-control datetimepicker-input',
                'data-target': '#datetimepicker1'
            })
        )

        date_end = forms.DateTimeField(
            required=False,
            input_formats=['%d/%m/%Y %H:%M'],
            widget=forms.DateTimeInput(attrs={
                'onchange': 'form.submit();',
                'class': 'form-control datetimepicker-input',
                'data-target': '#datetimepicker2'
            })
        )
