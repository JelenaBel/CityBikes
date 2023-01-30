from django.db import models


# creating Station model for a database
class Station (models.Model):
    f_id = models.IntegerField('Station id',  unique=True)
    station_id = models.IntegerField('Station id',  primary_key=True, unique=True)
    name_fin = models.CharField('Name fin', max_length=200)
    name_swd = models.CharField('Name swd', max_length=200)
    name_eng = models.CharField('Name eng', max_length=200)
    address_fin = models.CharField('Osoite fin', max_length=300)
    address_swd = models.CharField('Adress swd', max_length=300)
    city_fin = models.CharField('Kaupunki fin', max_length=100)
    city_swd = models.CharField('Stad swd', max_length=100)
    operator = models.CharField('Operaattor', max_length=200)
    capacity = models.IntegerField('Kapasiteet')
    coord_x = models.CharField('X', max_length=30)
    coord_y = models.CharField('Y', max_length=30)


    def __str__(self):
        return self.station_id


# creating Route model for a database
class Route(models.Model):
    route_id = models.IntegerField('Route id',  primary_key=True, unique = True)
    departure_time = models.DateTimeField('Departure time')
    return_time = models.DateTimeField('Return time')
    departure_station_id = models.ForeignKey(Station, on_delete=models.PROTECT, related_name='Departure_station_fk',  null=True)
    departure_station_name = models.CharField('Departure station name', max_length=600)
    return_station_id = models.ForeignKey(Station, on_delete=models.PROTECT, related_name='Return_station_fk', null=True)
    return_station_name = models.CharField('Return station name', max_length=600)
    covered_distance = models.FloatField('Covered distance (m)')
    duration = models.IntegerField('Duration (sec)')
    covered_distance_km = models.FloatField('Covered distance (km)', default='1')
    duration_min = models.FloatField('Duration (min)',  default='1')


    def __str__(self):
        return self.route_id


class MistakesStation(models.Model):
    mistake_station_id = models.CharField('Mistake Station id', max_length=16, primary_key=True, unique=True)
    info_line = models.CharField('Info line', max_length=600)

    def __str__(self):
        return self.mistake_station_id


class MistakesRoute(models.Model):
    mistake_route_id = models.CharField('Mistake route id', max_length=16, primary_key=True, unique=True)
    info_line = models.CharField('Info line', max_length=600)

    def __str__(self):
        return self.mistake_route_id








