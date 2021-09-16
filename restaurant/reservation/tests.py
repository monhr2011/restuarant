from django.db import IntegrityError
from django.test import TestCase
from reservation.models import Reservation, Table


class TableTestCase(TestCase):
    def setUp(self):
        Table.objects.create(number=1, number_of_seats=2)
        Table.objects.create(number=2, number_of_seats=3)
        Table.objects.create(number=3, number_of_seats=4)

    def test_table_number_duplicate(self):
        with self.assertRaises(IntegrityError):
            Table.objects.create(number=1, number_of_seats=5)

    def test_table_number_negative(self):
        with self.assertRaises(IntegrityError):
            Table.objects.create(number=-1, number_of_seats=5)


# Create your tests here.
