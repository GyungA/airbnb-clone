# Generated by Django 2.0 on 2018-01-08 07:06

import cities.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cities', '0010_adjust_unique_attributes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='city',
            name='country',
            field=models.ForeignKey(on_delete=cities.models.SET_NULL_OR_CASCADE, related_name='cities', to=settings.CITIES_COUNTRY_MODEL),
        ),
        migrations.AlterField(
            model_name='city',
            name='region',
            field=models.ForeignKey(blank=True, null=True, on_delete=cities.models.SET_NULL_OR_CASCADE, related_name='cities', to='cities.Region'),
        ),
        migrations.AlterField(
            model_name='city',
            name='subregion',
            field=models.ForeignKey(blank=True, null=True, on_delete=cities.models.SET_NULL_OR_CASCADE, related_name='cities', to='cities.Subregion'),
        ),
        migrations.AlterField(
            model_name='country',
            name='continent',
            field=models.ForeignKey(null=True, on_delete=cities.models.SET_NULL_OR_CASCADE, related_name='countries', to=settings.CITIES_CONTINENT_MODEL),
        ),
        migrations.AlterField(
            model_name='district',
            name='city',
            field=models.ForeignKey(on_delete=cities.models.SET_NULL_OR_CASCADE, related_name='districts', to=settings.CITIES_CITY_MODEL),
        ),
        migrations.AlterField(
            model_name='postalcode',
            name='city',
            field=models.ForeignKey(blank=True, null=True, on_delete=cities.models.SET_NULL_OR_CASCADE, related_name='postal_codes', to=settings.CITIES_CITY_MODEL),
        ),
        migrations.AlterField(
            model_name='postalcode',
            name='district',
            field=models.ForeignKey(blank=True, null=True, on_delete=cities.models.SET_NULL_OR_CASCADE, related_name='postal_codes', to='cities.District'),
        ),
        migrations.AlterField(
            model_name='postalcode',
            name='region',
            field=models.ForeignKey(blank=True, null=True, on_delete=cities.models.SET_NULL_OR_CASCADE, related_name='postal_codes', to='cities.Region'),
        ),
        migrations.AlterField(
            model_name='postalcode',
            name='subregion',
            field=models.ForeignKey(blank=True, null=True, on_delete=cities.models.SET_NULL_OR_CASCADE, related_name='postal_codes', to='cities.Subregion'),
        ),
        migrations.AlterField(
            model_name='region',
            name='country',
            field=models.ForeignKey(on_delete=cities.models.SET_NULL_OR_CASCADE, related_name='regions', to=settings.CITIES_COUNTRY_MODEL),
        ),
        migrations.AlterField(
            model_name='subregion',
            name='region',
            field=models.ForeignKey(on_delete=cities.models.SET_NULL_OR_CASCADE, related_name='subregions', to='cities.Region'),
        ),
    ]
