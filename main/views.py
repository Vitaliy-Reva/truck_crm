from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import *
from .serializer import *

#-------------------------------------------------------------------------------------------
# Transport CRUD
#-------------------------------------------------------------------------------------------
@api_view(['GET', 'POST'])
def transport_list(request):
    if request.method == 'GET':
        transports = Transport.objects.all()
        serializer = TransportSerializer(transports, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = TransportSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

@api_view(['GET', 'PUT', 'DELETE'])
def transport_detail(request, pk):
    try:
        transport = Transport.objects.get(pk=pk)
    except:
        return Response({"error": "Object not found"})
    
    if request.method == 'GET':
        serializer = TransportSerializer(transport)
        return Response(serializer.data)

    if request.method == 'PUT':
        serializer = TransportSerializer(transport, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    if request.method == 'DELETE':
        transport.delete()
        return Response()
    
#-------------------------------------------------------------------------------------------
# Driver CRUD
#-------------------------------------------------------------------------------------------
@api_view(['GET', 'POST'])
def driver_list(request):
    if request.method == 'GET':
        drivers = Driver.objects.all()
        serializer = DriverSerializer(drivers, many=True)
        return Response(serializer.data)
    
    if request.method == 'POST':
        serializer = DriverSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

@api_view(['GET', 'PUT', 'DELETE'])
def driver_detail(request, pk):
    try:
        driver = Driver.objects.get(pk=pk)
    except:
        return Response({"error": "Object not found"})
    
    if request.method == 'GET':
        serializer = DriverSerializer(driver)
        return Response(serializer.data)

    if request.method == 'PUT':
        serializer = DriverSerializer(driver, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    if request.method == 'DELETE':
        driver.delete()
        return Response()
    
#-------------------------------------------------------------------------------------------
# Trip CRUD
#-------------------------------------------------------------------------------------------
@api_view(['GET', 'POST'])
def trip_list(request):
    if request.method == 'GET':
        trips = Trip.objects.all()
        serializer = TripSerializer(trips, many=True)
        return Response(serializer.data)
    
    if request.method == 'POST':
        serializer = TripSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

@api_view(['GET', 'PUT', 'DELETE'])   
def trip_detail(request, pk):
    try:
        trip = Trip.objects.get(pk=pk)
    except:
        Response({"error": "Object not found"})
    
    if request.method == 'GET':
        serializer = TripSerializer(trip)
        return Response(serializer.data)
    
    if request.method == 'PUT':
        serializer = TripSerializer(trip, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
    if request.method == 'DELETE':
        trip.delete()
        return Response()
    
#-------------------------------------------------------------------------------------------
# FuelLog CRUD
#-------------------------------------------------------------------------------------------
@api_view(['GET', 'POST'])
def fuel_list(request):
    if request.method == 'GET':
        fuels = FuelLog.objects.all()
        serializer = FuelLogSerializer(fuels, many=True)
        return Response(serializer.data)
    
    if request.method == 'POST':
        serializer = FuelLogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
@api_view(['GET', 'PUT', 'DELETE'])
def fuel_detail(request, pk):
    try:
        fuel = FuelLog.objects.get(pk=pk)
    except:
        return Response({"error": "Object not found"})
    
    if request.method == 'GET':
        serializer = FuelLogSerializer(fuel)
        return Response(serializer.data)
    
    if request.method == 'PUT':
        serializer = FuelLogSerializer(fuel, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
    if request.method == 'DELETE':
        fuel.delete()
        return Response()

#-------------------------------------------------------------------------------------------
# Maintenance CRUD
#-------------------------------------------------------------------------------------------
@api_view(['GET', 'POST'])
def maintenance_list(request):
    if request.method == 'GET':
        maintenance = Maintenance.objects.all()
        serializer = MaintenanceSerializer(maintenance, many=True)
        return Response(serializer.data)
    
    if request.method == 'POST':
        serializer = MaintenanceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
@api_view(['GET', 'PUT', 'DELETE'])
def maintenance_detail(request, pk):
    try:
        maintenance = Maintenance.objects.get(pk=pk)
    except:
        return Response({"error": "Object not found"})
    
    if request.method == 'GET':
        serializer = MaintenanceSerializer(maintenance)
        return Response(serializer.data)
    
    if request.method == 'PUT':
        serializer = MaintenanceSerializer(maintenance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
    if request.method == 'DELETE':
        maintenance.delete()
        return Response()