from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import *
from .serializer import *

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