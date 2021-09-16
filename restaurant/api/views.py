import datetime
import logging

from django.utils.dateparse import parse_time
from rest_framework import mixins, generics
from rest_framework.exceptions import ValidationError
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated

from api.auth import IsAdmin, IsEmployee
from api.mixins import ListModelMixin, CreateModelMixin
from api.pagination import PageNumberPagination
from reservation.models import Table, Reservation
from reservation.serializers import TableSerializer, ReservationSerializer, ReserveTodaySerializer

logger = logging.getLogger('django.request')


class APIError404(generics.GenericAPIView):
    """
    Generic 404 Page to handle non-existing urls
    """

    permission_classes = [IsAuthenticated, ]

    def dispatch(self, request, *args, **kwargs):
        request.method = 'GET'
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        raise generics.Http404("Invalid Url")


class BaseAdminAPIView(generics.GenericAPIView):
    """
    Generic AdminAPIView to specify pages for admin
    """
    permission_classes = [IsAdmin]

    def get_permissions(self):
        return super().get_permissions()


class BaseEmployeeAPIView(generics.GenericAPIView):
    permission_classes = [IsEmployee]


class BaseStaffAPIView(generics.GenericAPIView):
    permission_classes = [IsEmployee | IsAdmin]


class TableList(ListModelMixin,
                CreateModelMixin,
                BaseAdminAPIView):
    queryset = Table.objects.all().order_by('number')
    serializer_class = TableSerializer

    def get(self, request, *args, **kwargs):
        data = self.list(request, *args, **kwargs)
        return data

    def post(self, request, *args, **kwargs):
        data = self.create(request, *args, **kwargs)
        return data

    def get_serializer(self, *args, **kwargs):
        return super().get_serializer(*args, **kwargs)

    def delete(self, request, *args, **kwargs):
        table = self.get_object()
        if table.reservations.exists():
            raise ValidationError("Cannot delete that has reservations")
        return self.destroy(request, *args, **kwargs)



class TableDelete(mixins.DestroyModelMixin,
                  BaseAdminAPIView):
    queryset = Table.objects.all().order_by('number')
    serializer_class = TableSerializer

    def delete(self, request, *args, **kwargs):
        table = self.get_object()
        if table.reservations.exists():
            raise ValidationError("Cannot delete that has reservations")
        return self.destroy(request, *args, **kwargs)


# region Reservation endpoints

class CheckAvailableTimeSlots(BaseStaffAPIView):
    pass


class TodayReservations(ListModelMixin,
                        mixins.DestroyModelMixin,
                        BaseStaffAPIView):
    def get_object(self):
        return super().get_object()

    queryset = Reservation.today_reservations()
    serializer_class = ReservationSerializer

    def get_queryset(self):
        return super().get_queryset()

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = ReserveTodaySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        start_time = parse_time(serializer.data.get('start_time'))
        end_time = parse_time(serializer.data.get('end_time'))
        try:
            table = Table.objects.get(number=serializer.data.get('table_no'))
        except:
            raise ValidationError({'table_no':"Table number is not valid"})
        return table.reserve(
            start_time=start_time,
            end_time=end_time,
            reserved_by=request.user.staff
        )

    def delete(self, request, *args, **kwargs):
        pass


class AllReservations(ListModelMixin,
                      BaseAdminAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    pagination_class = PageNumberPagination
    filter_backends = [OrderingFilter]
    ordering_fields = ['table_number']

    def get_queryset(self):

        return super().get_queryset()

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class DeleteReservation(BaseStaffAPIView):
    pass

# endregion
