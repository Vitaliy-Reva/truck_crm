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
from .services.order_service import OrderService
from .services.payment_service import PaymentService
from .services.item_list import get_items
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
        serializer = TransportSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        TransportService.create_transport(data=serializer.validated_data)
        return Response(serializer.data, status=201)
        
@api_view(['GET', 'PATCH', 'DELETE'])
def transport_detail(request, pk):
    try:
        transport = Transport.objects.get(pk=pk)
    except Transport.DoesNotExist:
        return Response({"error": "Object not found"})
    
    if request.method == 'GET':
        serializer = TransportSerializer(transport)
        return Response(serializer.data)

    if request.method == 'PATCH':
        serializer = TransportSerializer(transport, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        TransportService.update_transport(data=serializer.validated_data, transport=transport)
        return Response(serializer.data, status=200)

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
        serializer = DriverSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        DriverService.driver_create(data=serializer.validated_data)
        return Response(serializer.data, status=201)

@api_view(['GET', 'PATCH', 'DELETE'])
def driver_detail(request, pk):
    try:
        driver = Driver.objects.get(pk=pk)
    except Driver.DoesNotExist:
        return Response({"error": "Object not found"})
    
    if request.method == 'GET':
        serializer = DriverSerializer(driver)
        return Response(serializer.data)

    if request.method == 'PATCH':
        serializer = DriverSerializer(driver, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        DriverService.driver_update(data=serializer.validated_data, driver=driver)
        return Response(serializer.data, status=200)

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
        serializer = ClientSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        ClientService.create_client(data=serializer.validated_data)
        return Response(serializer.data, status=201)

@api_view(['GET', 'PATCH', 'DELETE'])
def client_detail(request, pk):
    try:
        client = Client.objects.get(pk=pk)
    except Client.DoesNotExist:
        return Response(ClientSerializer(client).data)
    
    if request.method == 'GET':
        serializer = ClientSerializer(client)
        return Response(serializer.data)
    
    if request.method == 'PATCH':
        serializer = ClientSerializer(client, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        ClientService.update_client(data=serializer.validated_data, client=client)
        return Response(serializer.data, status=200)

    if request.method == 'DELETE':
        client.delete()
        return Response()

#-------------------------------------------------------------------------------------------
# Order CRUD
#-------------------------------------------------------------------------------------------   
@extend_schema(
    request=OrderSerializer,
    responses=OrderSerializer
)

@api_view(['GET', 'POST'])
def order_list(request):
    if request.method == 'GET':
        order = Order.objects.all()
        serializer = OrderSerializer(order, many=True)
        return Response(serializer.data)
    
    if request.method == 'POST':
        client_id = request.data.get('client_id')
        client = Client.objects.get(pk=client_id)
        
        serializer = OrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        OrderService.create_order(data=serializer.validated_data, client=client)
        return Response(serializer.data, status=201)
    
@api_view(['GET', 'PATCH', 'DELETE'])
def order_detail(request, pk):
    try:
        order = Order.objects.get(pk=pk)
    except Order.DoesNotExist:
        Response({"error": "Object not found"})
    
    if request.method == 'GET':
        serializer = OrderSerializer(order)
        return Response(serializer.data, status=200)
    
    if request.method == 'PATCH':
        client_id = request.data.get('client_id')
        client = Client.objects.get(pk=client_id)

        serializer = OrderSerializer(order, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        OrderService.update_order(data=serializer.validated_data, order=order, client=client)
        return Response(serializer.data, status=201)
    
    if request.method == 'DELETE':
        order.delete()
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
        trip = Trip.objects.all()
        serializer = TripSerializer(trip, many=True)
        return Response(serializer.data)
    
    if request.method == 'POST':
        driver_id = request.data.get("driver_id")
        driver = Driver.objects.get(pk=driver_id)
        transport_id = request.data.get("transport_id")
        transport = Transport.objects.get(pk=transport_id)
        client_id = request.data.get("client_id")
        client = Client.objects.get(pk=client_id)
        order_id = request.data.get("order_id")
        order = Order.objects.get(pk=order_id)

        serializer = TripSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        TripService.trip_create(data=serializer.validated_data, driver=driver, transport=transport, client=client, order=order)
        return Response(serializer.data, status=201)

@api_view(['GET', 'PATCH', 'DELETE'])   
def trip_detail(request, pk):
    try:
        trip = Trip.objects.get(pk=pk)
    except Trip.DoesNotExist:
        Response({"error": "Object not found"})
    
    if request.method == 'GET':
        serializer = TripSerializer(trip)
        return Response(serializer.data)
    
    if request.method == 'PATCH':
        driver_id = request.data.get("driver_id")
        driver = Driver.objects.get(pk=driver_id)
        transport_id = request.data.get("transport_id")
        transport = Transport.objects.get(pk=transport_id)
        client_id = request.data.get("client_id")
        client = Client.objects.get(pk=client_id)
        order_id = request.data.get("order_id")
        order = Order.objects.get(pk=order_id)

        serializer = TripSerializer(trip, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        TripService.trip_update(data=serializer.validated_data, trip=trip, driver=driver, transport=transport, client=client, order=order)
        return Response(serializer.data, status=200)
    
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

        serializer = FuelLogSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        FuelLogService.fuellog_create(data=serializer.validated_data, trip=trip, transport=transport)
        return Response(serializer.data, status=201)
    
@api_view(['GET', 'PATCH', 'DELETE'])
def fuel_detail(request, pk):
    try:
        fuellog = FuelLog.objects.get(pk=pk)
    except FuelLog.DoesNotExist:
        return Response({"error": "Object not found"})
    
    if request.method == 'GET':
        serializer = FuelLogSerializer(fuellog)
        return Response(serializer.data)
    
    if request.method == 'PATCH':
        trip_id = request.data.get("trip_id")
        trip = Trip.objects.get(pk=trip_id)
        transport_id = request.data.get("transport_id")
        transport = Transport.objects.get(pk=transport_id)

        serializer = FuelLogSerializer(fuellog, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        FuelLogService.fuellog_update(data=serializer.validated_data, fuellog=fuellog, trip=trip, transport=transport)
        return Response(serializer.data, status=200)
    
    if request.method == 'DELETE':
        fuellog.delete()
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

        serializer = MaintenanceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        MaintenanceService.maintenance_create(data=serializer.validated_data, transport=transport)
        return Response(serializer.data, status=201)
    
@api_view(['GET', 'PATCH', 'DELETE'])
def maintenance_detail(request, pk):
    try:
        maintenance = Maintenance.objects.get(pk=pk)
    except Maintenance.DoesNotExist:
        return Response({"error": "Object not found"})
    
    if request.method == 'GET':
        serializer = MaintenanceSerializer(maintenance)
        return Response(serializer.data)
    
    if request.method == 'PATCH':
        transport_id = request.data.get("transport_id")
        transport = Transport.objects.get(pk=transport_id)

        serializer = MaintenanceSerializer(maintenance, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            MaintenanceService.maintenance_update(data=serializer.validated_data, maintenance=maintenance, transport=transport)
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)
    
    if request.method == 'DELETE':
        maintenance.delete()
        return Response()

#-------------------------------------------------------------------------------------------
# Payment
#-------------------------------------------------------------------------------------------

@api_view(['POST'])
def load_payment(request):
    if request.method == 'POST':
        payment = request.FILES.get('payment_register')
        PaymentService.payment_process(payment)
        return Response()

#-------------------------------------------------------------------------------------------
# NoPayedOrder
#-------------------------------------------------------------------------------------------

@api_view(['GET'])
def nopayment(request):
    if request.method == 'GET':
        nopayment = NoPayedOrder.objects.all()
        serializer = NoPayedOrderSerializer(nopayment, many=True)
        return Response(serializer.data, status=200)

@api_view(['GET', 'DELETE'])
def nopaymentdetail(request, pk):
    if request.method == 'GET':
        try:
            nopayment = NoPayedOrder.objects.get(pk=pk)
        except NoPayedOrder.DoesNotExist:
            return Response({"error": "Object not found"})
    
    if request.method == 'DELETE':
        nopayment.delete()
        return Response()

#-------------------------------------------------------------------------------------------
# GetOrderDoc
#-------------------------------------------------------------------------------------------

@api_view(['GET'])
def get_order_doc(request):
    if request.method == 'GET':
        orders = Trip.objects.all()
        get_items(orders)
        return Response(status=200)

@api_view(['GET'])
def get_order_doc_by_id(request, pk):
    if request.method == 'GET':
        try:
            order = Trip.objects.get(pk=pk)
        except Trip.DoesNotExist:
            return Response({"error": "Object not found"})
        
        get_items(order)
        return Response(status=200)