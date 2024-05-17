from django.db.models import Count, F
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets

from station.models import Bus, Trip, Ticket, Facility, Order
from station.serializers import (
    BusSerializer, TripSerializer, TicketSerializer, TripListSerializer,
    FacilitySerializer, BusListSerializer, BusRetrieveSerializer,
    TripRetrieveSerializer, OrderSerializer, OrderListSerializer,
    BusImageSerializer
)


class BusSetPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 20


class BusViewSet(viewsets.ModelViewSet):
    queryset = Bus.objects.all()
    pagination_class = BusSetPagination

    @staticmethod
    def _params_to_ints(query_string):
        """Converts a string of format '1,2,3' to a list of [1,2,3]"""
        return [int(str_id) for str_id in query_string.split(",")]

    def get_serializer_class(self):
        if self.action == "list":
            return BusListSerializer
        if self.action == "retrieve":
            return BusRetrieveSerializer
        elif self.action == "upload_image":
            return BusImageSerializer
        return BusSerializer

    def get_queryset(self):
        queryset = self.queryset

        facilities = self.request.query_params.get('facilities')

        if facilities:
            facilities = self._params_to_ints(facilities)
            queryset = queryset.filter(facilities__id__in=facilities)

        if self.action in ("list", "retrieve"):
            return queryset.prefetch_related("facilities")
        return queryset.distinct()

    @action(
        methods=["POST"],
        detail=True,
        permission_classes=[IsAdminUser],
        url_path="upload-image"
    )
    def upload_image(self, request, pk=None):
        bus = self.get_object()
        serializer = self.get_serializer(bus, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "facilities",
                type={"type": "array", "items": {"type": "number"}},
                description="Filter by facilities id ex(?facilities=2,3)"
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        """Get list of buses"""
        return super().list(request, *args, **kwargs)


class TripViewSet(viewsets.ModelViewSet):
    queryset = Trip.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return TripListSerializer
        if self.action == "retrieve":
            return TripRetrieveSerializer
        return TripSerializer

    def get_queryset(self):
        queryset = self.queryset
        if self.action == "list":
            queryset = (
                queryset
                .select_related()
                .annotate(tickets_available=F("bus__num_seats") - Count("tickets"))
            )
        if self.action == "retrieve":
            return queryset.select_related()
        return queryset.order_by("id")


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer


class FacilityViewSet(viewsets.ModelViewSet):
    queryset = Facility.objects.all()
    serializer_class = FacilitySerializer


class OrderSetPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 20


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    pagination_class = OrderSetPagination

    def get_serializer_class(self):
        serializer_class = self.serializer_class

        if self.action == "list":
            serializer_class = OrderListSerializer

        return serializer_class

    def get_queryset(self):
        queryset = self.queryset.filter(user=self.request.user)

        if self.action == "list":
            queryset = queryset.prefetch_related("tickets__trip__bus")

        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
