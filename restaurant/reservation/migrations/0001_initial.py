# Generated by Django 3.2.7 on 2021-09-15 14:15

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('staff', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Table',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.PositiveIntegerField(verbose_name='Table Number')),
                ('number_of_seats', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(12), django.core.validators.MinValueValidator(1)], verbose_name='Number of seats')),
            ],
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField(verbose_name='Start time')),
                ('end_time', models.DateTimeField(verbose_name='End time')),
                ('reserved_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='staff.staff')),
                ('table', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='reservations', to='reservation.table', verbose_name='Table')),
            ],
        ),
    ]
