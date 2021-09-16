from django.urls import path, include, re_path
from rest_framework import routers

from api import views

router = routers.SimpleRouter()

app_name = "api"
urlpatterns = [
    path('tables', views.TableList.as_view(), name="tables"),
    path('reservations/available', views.CheckAvailableTimeSlots.as_view(), name="available-reservation"),
    path('reservations', views.TodayReservations.as_view(), name="reservations"),
    path('reservations/all', views.AllReservations.as_view(), name="all-reservations"),
    re_path(r'[\s\S]+', views.APIError404.as_view(), )  # Return API response instead of django http 404
]
