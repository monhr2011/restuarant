import datetime
from datetime import timedelta

from django.conf import settings
from django.db import models
from django.db.models import Min
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from reservation.validators import validate_max_number_of_seats, validate_min_number_of_seats
from staff.models import Staff


# TODO check whether 'Table Number' should not be duplicate across all tables or for specific number of seats
# Examples:
#   Case #1: Table(1, 12) , Table(2, 11), Table(3, 12) ...etc (# We are going to assume this table)
#   Case #2: Table(1, 12) , Table(1, 11), Table(2, 12) ...etc
class Table(models.Model):
    number = models.PositiveIntegerField(verbose_name=_("Table Number"), null=False, blank=False, unique=True)
    number_of_seats = models.PositiveIntegerField(verbose_name=_("Number of seats"), null=False, blank=False,
                                                  validators=[
                                                      validate_max_number_of_seats,
                                                      validate_min_number_of_seats,
                                                  ])

    @staticmethod
    def get_available_tables(start_time: datetime.time, end_time: datetime.time, required_seats: int,
                             reservation_date: datetime.date = None):
        if not reservation_date:
            reservation_date = timezone.now().date()
        if required_seats < 1:
            raise ValueError("required_seats cannot be less than 1")
        reservations = Reservation.reservation_date(reservation_date)
        start_date = datetime.datetime.combine(
            date=reservation_date,
            time=start_time,
            tzinfo=timezone.now().tzinfo
        )
        end_date = datetime.datetime.combine(
            date=reservation_date,
            time=end_time,
            tzinfo=timezone.now().tzinfo
        )
        if start_date > end_date:
            raise ValueError("start_date cannot be greater than end_date")
        reservations = reservations.filter(end_time__gte=start_date, start_time__lte=end_date)
        minimum_required_seats = Table.get_minimum_possible_seats(required_seats)
        available_tables = Table.objects.filter(number_of_seats=minimum_required_seats).exclude(
            reservations__in=reservations
        )
        return available_tables

    @staticmethod
    def get_minimum_possible_seats(required_seats: int):
        if required_seats < 1:
            return 0
        allowed_possible_tables = Table.objects.filter(number_of_seats__gte=required_seats)
        if allowed_possible_tables.exists():
            return allowed_possible_tables.aggregate(
                minimum_possible_seat=Min('number_of_seats')).get("minimum_possible_seat")
        else:
            return 0

    @staticmethod
    def get_available_times(required_seats: int, reservation_date: datetime.date = None):
        if not reservation_date:
            reservation_date = timezone.now().date()

    def reserve(self, start_time: datetime.time, end_time: datetime.time, reservation_date: datetime.date = None,
                reserved_by=None):
        if not reservation_date:
            reservation_date = timezone.now().date()
        if self not in Table.get_available_tables(start_time=start_time,
                                                  end_time=end_time,
                                                  required_seats=self.number_of_seats,
                                                  reservation_date=reservation_date):
            raise ValueError("Table cannot be reserved at the allocated time")
        else:
            start_date = datetime.datetime.combine(
                date=reservation_date,
                time=start_time,
                tzinfo=timezone.now().tzinfo
            )
            end_date = datetime.datetime.combine(
                date=reservation_date,
                time=end_time,
                tzinfo=timezone.now().tzinfo
            )
            reservation = Reservation(
                start_time=start_date,
                end_time=end_date,
                table=self,
                reserved_by=reserved_by,
            )
            reservation.save()
            return reservation

    def __str__(self):
        try:
            return "Table #{}, Number of seats: {}".format(self.number, self.number_of_seats)
        except:
            return super().__str__()


class Reservation(models.Model):
    table = models.ForeignKey(Table, verbose_name=_("Table"), on_delete=models.PROTECT, related_name='reservations',
                              null=False, blank=False)
    start_time = models.DateTimeField(verbose_name=_("Start time"), null=False, blank=False)
    end_time = models.DateTimeField(verbose_name=_("End time"), null=False, blank=False)
    reserved_by = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, blank=False)

    # inclusive reservation time
    @staticmethod
    def reservation_range(start_date: datetime.date, end_date: datetime.date):
        if start_date > end_date:
            raise ValueError("Start Date cannot be greater than end date")
        reservations = Reservation.objects.filter(start_time__lte=end_date + timedelta(days=1),
                                                  end_time__gte=start_date)
        return reservations

    @staticmethod
    def reservation_date(date: datetime.date):
        return Reservation.reservation_range(start_date=date, end_date=date)

    @staticmethod
    def today_reservations():
        return Reservation.reservation_date(timezone.now().date())

    def __str__(self):
        try:
            return _("Table {}: {} - {}").format(self.table.number, self.start_time, self.end_time)
        except:
            return super().__str__()
