# Generated by Django 4.1.5 on 2023-01-23 20:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_alter_route_covered_distance_alter_route_duration_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='route',
            name='covered_distance',
            field=models.IntegerField(verbose_name='Covered distance (m)'),
        ),
        migrations.AlterField(
            model_name='route',
            name='duration',
            field=models.IntegerField(verbose_name='Duration (sec)'),
        ),
        migrations.AlterField(
            model_name='route',
            name='route_id',
            field=models.IntegerField(primary_key=True, serialize=False, unique=True, verbose_name='Route id'),
        ),
        migrations.AlterField(
            model_name='station',
            name='capacity',
            field=models.IntegerField(verbose_name='Kapasiteet'),
        ),
        migrations.AlterField(
            model_name='station',
            name='f_id',
            field=models.IntegerField(unique=True, verbose_name='Station id'),
        ),
        migrations.AlterField(
            model_name='station',
            name='station_id',
            field=models.IntegerField(primary_key=True, serialize=False, unique=True, verbose_name='Station id'),
        ),
    ]