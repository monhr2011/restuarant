from django.contrib import admin

from reservation.models import Table, Reservation

admin.site.register(Table)
admin.site.register(Reservation)
