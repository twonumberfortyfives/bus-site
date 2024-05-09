from django.urls import path
from station.views import bus_list, bus_detail


urlpatterns = [
    path('buses/', bus_list, name="bus-list"),
    path('buses/<int:pk>/', bus_detail, name="bus-detail")
]

app_name = "station"
