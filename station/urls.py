from django.urls import path, include
from rest_framework import routers

from station.views import BusViewSet, TripViewSet, TicketViewSet, FacilityViewSet

# simplifying urls

router = routers.DefaultRouter()
router.register("buses", BusViewSet)
router.register("trips", TripViewSet)
router.register("tickets", TicketViewSet)
router.register("facilities", FacilityViewSet)

# urlpatterns = router.urls
# _____________________________________________________________________________________________________________________
urlpatterns = [
    path("", include(router.urls))
]

# _____________________________________________________________________________________________________________________
# bus_list = BusViewSet.as_view(actions={"get": "list", "post": "create"})
# bus_detail = BusViewSet.as_view(
#     actions={
#         "get": "retrieve",
#         "put": "update",
#         "patch": "partial_update",
#         "delete": "destroy"
#     }
# )
#
# urlpatterns = [
#     path('buses/', bus_list, name="bus-list"),
#     path('buses/<int:pk>/', bus_detail, name="bus-detail")
# ]
#
app_name = "station"
