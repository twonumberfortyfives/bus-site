from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics, mixins, viewsets

from station.models import Bus
from station.serializers import BusSerializer

# USING MANUAL VIEW FUNC TO MANIPULATE REQUESTS
# ___________________________________________________________________
# @api_view(["GET", "POST"])
# def bus_list(request):
#     if request.method == 'GET':
#         buses = Bus.objects.all()
#         serializer = BusSerializer(buses, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#     elif request.method == "POST":
#         serializer = BusSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# _____________________________________________________________________________
#
# SIMPLE WAY AND MORE CLEAN BY USING CLASS VIEWS
#
# class BusListView(APIView):
#     def get(self, request) -> Response:
#         buses = Bus.objects.all()
#         serializer = BusSerializer(buses, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#
#     def post(self, request) -> Response:
#         serializer = BusSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# ___________________________________________________________________________________
#
#  USING GenericAPIView TO USE OTHER MIXINS FOR CRUD
#
# class BusListView(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin):
#     queryset = Bus.objects.all()
#     serializer_class = BusSerializer
#
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)
#
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)

# USING generics views LIBRARY WHAT CONTAINS SHORTEST WAY FOR IMPLEMENTATION CRUD


# class BusListView(generics.ListCreateAPIView):
#     queryset = Bus.objects.all()
#     serializer_class = BusSerializer
#
#
# class BusDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Bus.objects.all()
#     serializer_class = BusSerializer

# _____________________________________________________________________________________________________________________
# @api_view(["GET", "PUT", "DELETE"])
# def bus_detail(request, pk: int):
#     bus = get_object_or_404(Bus, pk=pk)
#     if request.method == 'GET':
#         serializer = BusSerializer(bus)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#     elif request.method == "PUT":
#         serializer = BusSerializer(bus, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     elif request.method == "DELETE":
#         bus.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

# _____________________________________________________________________________________________________________________
# class BusDetailView(APIView):
#     def get_object(self, pk: int) -> Bus:
#         return Bus.objects.get(pk=pk)
#
#     def get(self, request, pk: int) -> Response:
#         serializer = BusSerializer(self.get_object(pk=pk))
#         return Response(serializer.data, status=status.HTTP_200_OK)
#
#     def put(self, request, pk: int) -> Response:
#         serializer = BusSerializer(self.get_object(pk=pk),
#                                    data=request.data)  # possible to implement partial parameter for PATCH method
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#
#     def delete(self, request, pk: int) -> Response:
#         self.get_object(pk=pk).delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
#
# _____________________________________________________________________________________________________________________
#
# class BusDetailView(
#     generics.GenericAPIView,
#     mixins.RetrieveModelMixin,
#     mixins.UpdateModelMixin,
#     mixins.DestroyModelMixin,
# ):
#     queryset = Bus.objects.all()
#     serializer_class = BusSerializer
#
#     def get(self, request, *args, **kwargs) -> Bus:
#         return self.retrieve(request, *args, **kwargs)
#
#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)
#
#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)
# _____________________________________________________________________________________________________________________
# CREATION VIEWS WITH viewsets AND CHANGING URLS IN THE APP (USE ACTIONS ATTRIBUTE )
# ALSO IS POSSIBLE TO COMBINE TWO CLASSES IN ONE

# class BusListView(
#     viewsets.GenericViewSet,
#     mixins.ListModelMixin,
#     mixins.CreateModelMixin
# ):
#     queryset = Bus.objects.all()
#     serializer_class = BusSerializer
#
#
# class BusDetailView(
#     viewsets.GenericViewSet,
#     mixins.RetrieveModelMixin,
#     mixins.UpdateModelMixin,
#     mixins.DestroyModelMixin
# ):
#     queryset = Bus.objects.all()
#     serializer_class = BusSerializer
# _____________________________________________________________________________________________________________________
#
# MERGED INTO ONE CLASS (LINKS ARE CHANGED
# USED viewsets.ModelViewSet what contains all views

class BusViewSet(
    viewsets.ModelViewSet,
):
    queryset = Bus.objects.all()
    serializer_class = BusSerializer
