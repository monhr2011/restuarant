from rest_framework import serializers

from reservation.models import Table, Reservation


class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = ['number', 'number_of_seats']


class TodayReservationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ['start_time', 'end_time', 'table_no']


class ReserveTodaySerializer(serializers.Serializer):
    start_time = serializers.TimeField()
    end_time = serializers.TimeField()
    table_no = serializers.IntegerField()


class ReservationSerializer(serializers.ModelSerializer):
    table_number = serializers.SerializerMethodField()

    class Meta:
        model = Reservation
        fields = '__all__'

    def get_table_number(self, reservation):
        return reservation.table.number
