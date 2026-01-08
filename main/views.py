from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import *
from .serializer import *
from .services.transport_service import TransportService
from .services.driver_service import DriverService
from .services.client_service import ClientService
from .services.trip_service import TripService
from .services.fuellog_service import FuelLogService
from .services.maintenance_service import MaintenanceService
from drf_spectacular.utils import extend_schema

#-------------------------------------------------------------------------------------------
# Transport CRUD
#-------------------------------------------------------------------------------------------
@extend_schema(
    request=TransportSerializer,
    responses=TransportSerializer
)

@api_view(['GET', 'POST'])
def transport_list(request):
    if request.method == 'GET':
        transports = Transport.objects.all()
        serializer = TransportSerializer(transports, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        transport = TransportService.create_transport(request.data)
        serializer = TransportSerializer(transport, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)
        
@api_view(['GET', 'PUT', 'DELETE'])
def transport_detail(request, pk):
    try:
        transport = Transport.objects.get(pk=pk)
    except Transport.DoesNotExist:
        return Response({"error": "Object not found"})
    
    if request.method == 'GET':
        serializer = TransportSerializer(transport)
        return Response(serializer.data)

    if request.method == 'PUT':
        transport = TransportService.update_transport(data=request.data, transport=transport, new_mileage=request.data["mileage"])
        return Response(TransportSerializer(transport).data)

    if request.method == 'DELETE':
        transport.delete()
        return Response()
    
#-------------------------------------------------------------------------------------------
# Driver CRUD
#-------------------------------------------------------------------------------------------
@extend_schema(
    request=DriverSerializer,
    responses=DriverSerializer
)

@api_view(['GET', 'POST'])
def driver_list(request):
    if request.method == 'GET':
        drivers = Driver.objects.all()
        serializer = DriverSerializer(drivers, many=True)
        return Response(serializer.data)
    
    if request.method == 'POST':
        driver = DriverService.driver_create(request.data)
        return Response(DriverSerializer(driver).data)

@api_view(['GET', 'PUT', 'DELETE'])
def driver_detail(request, pk):
    try:
        driver = Driver.objects.get(pk=pk)
    except Driver.DoesNotExist:
        return Response({"error": "Object not found"})
    
    if request.method == 'GET':
        serializer = DriverSerializer(driver)
        return Response(serializer.data)

    if request.method == 'PUT':
        driver = DriverService.driver_update(driver=driver)
        return Response(DriverSerializer(driver).data)

    if request.method == 'DELETE':
        driver.delete()
        return Response()
    
#-------------------------------------------------------------------------------------------
# Client CRUD
#-------------------------------------------------------------------------------------------
@extend_schema(
    request=ClientSerializer,
    responses=ClientSerializer
)

@api_view(['GET', 'POST'])
def client_list(request):
    if request.method == 'GET':
        clients = Client.objects.all()
        serializer = ClientSerializer(clients, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        client = ClientService.created_client(data=request.data)
        return Response(ClientSerializer(client).data)

@api_view(['GET', 'PUT', 'DELETE'])
def client_detail(request, pk):
    try:
        client = Client.objects.get(pk=pk)
    except Client.DoesNotExist:
        return Response(ClientSerializer(client).data)
    
    if request.method == 'GET':
        serializer = ClientSerializer(client)
        return Response(serializer.data)
    
    if request.method == 'PUT':
        client = ClientService.update_client(client=client)
        return Response(ClientSerializer(client).data)

    if request.method == 'DELETE':
        client.delete()
        return Response()
    
#-------------------------------------------------------------------------------------------
# Trip CRUD
#-------------------------------------------------------------------------------------------
@extend_schema(
    request=TripSerializer,
    responses=TripSerializer
)

@api_view(['GET', 'POST'])
def trip_list(request):
    if request.method == 'GET':
        trips = Trip.objects.all()
        serializer = TripSerializer(trips, many=True)
        return Response(serializer.data)
    
    if request.method == 'POST':
        driver_id = request.data.get("driver_id")
        driver = Driver.objects.get(pk=driver_id)
        transport_id = request.data.get("transport_id")
        transport = Transport.objects.get(pk=transport_id)
        client_id = request.data.get("client_id")
        client = Client.objects.get(pk=client_id)

        trip = TripService.trip_create(data=request.data, driver=driver, transport=transport, client=client)
        return Response(TripSerializer(trip).data)

@api_view(['GET', 'PUT', 'DELETE'])   
def trip_detail(request, pk):
    try:
        trip = Trip.objects.get(pk=pk)
    except Trip.DoesNotExist:
        Response({"error": "Object not found"})
    
    if request.method == 'GET':
        serializer = TripSerializer(trip)
        return Response(serializer.data)
    
    if request.method == 'PUT':
        driver_id = request.data.get("driver_id")
        driver = Driver.objects.get(pk=driver_id)
        transport_id = request.data.get("transport_id")
        transport = Transport.objects.get(pk=transport_id)
        client_id = request.data.get("client_id")
        client = Client.objects.get(pk=client_id)

        trip = TripService.trip_update(trip, data=request.data, driver=driver, transport=transport, client=client)
        return Response(TripSerializer(trip).data)
    
    if request.method == 'DELETE':
        trip.delete()
        return Response()
    
#-------------------------------------------------------------------------------------------
# FuelLog CRUD
#-------------------------------------------------------------------------------------------
@extend_schema(
    request=FuelLogSerializer,
    responses=FuelLogSerializer
)

@api_view(['GET', 'POST'])
def fuel_list(request):
    if request.method == 'GET':
        fuels = FuelLog.objects.all()
        serializer = FuelLogSerializer(fuels, many=True)
        return Response(serializer.data)
    
    if request.method == 'POST':
        trip_id = request.data.get("trip_id")
        trip = Trip.objects.get(pk=trip_id)
        transport_id = request.data.get("transport_id")
        transport = Transport.objects.get(pk=transport_id)
        fuellog = FuelLogService.fuellog_create(request.data, trip=trip, transport=transport)
        return Response(FuelLogSerializer(fuellog).data)
    
@api_view(['GET', 'PUT', 'DELETE'])
def fuel_detail(request, pk):
    try:
        fuellog = FuelLog.objects.get(pk=pk)
    except FuelLog.DoesNotExist:
        return Response({"error": "Object not found"})
    
    if request.method == 'GET':
        serializer = FuelLogSerializer(fuellog)
        return Response(serializer.data)
    
    if request.method == 'PUT':
        trip_id = request.data.get("trip_id")
        trip = Trip.objects.get(pk=trip_id)
        transport_id = request.data.get("transport_id")
        transport = Transport.objects.get(pk=transport_id)
        fuellog = FuelLogService.fuellog_update(fuellog=fuellog, data=request.data, trip=trip, transport=transport)
        return Response(FuelLogSerializer(fuellog).data)
    
    if request.method == 'DELETE':
        trip_id = request.data.get("trip_id")
        trip = Trip.objects.get(pk=trip_id)
        transport_id = request.data.get("transport_id")
        transport = Transport.objects.get(pk=transport_id)
        FuelLogService.fuel_delete(data=request.data, fuellog=fuellog, trip=trip, transport=transport)
        return Response()

#-------------------------------------------------------------------------------------------
# Maintenance CRUD
#-------------------------------------------------------------------------------------------
@extend_schema(
    request=MaintenanceSerializer,
    responses=MaintenanceSerializer
)

@api_view(['GET', 'POST'])
def maintenance_list(request):
    if request.method == 'GET':
        maintenance = Maintenance.objects.all()
        serializer = MaintenanceSerializer(maintenance, many=True)
        return Response(serializer.data)
    
    if request.method == 'POST':
        transport_id = request.data.get("transport_id")
        transport = Transport.objects.get(pk=transport_id)
        maintenance = MaintenanceService.maintenance_create(data=request.data, transport=transport)
        return Response(MaintenanceSerializer(maintenance).data)
    
@api_view(['GET', 'PUT', 'DELETE'])
def maintenance_detail(request, pk):
    try:
        maintenance = Maintenance.objects.get(pk=pk)
    except Maintenance.DoesNotExist:
        return Response({"error": "Object not found"})
    
    if request.method == 'GET':
        serializer = MaintenanceSerializer(maintenance)
        return Response(serializer.data)
    
    if request.method == 'PUT':
        transport_id = request.data.get("transport_id")
        transport = Transport.objects.get(pk=transport_id)
        maintenance = MaintenanceService.maintenance_update(data=request.data, maintenance=maintenance, transport=transport)
        return Response(MaintenanceSerializer(maintenance).data)
    
    if request.method == 'DELETE':
        maintenance.delete()
        return Response()