#from django.shortcuts import render
from rest_framework import viewsets
from ecommapp.serializers import *
from ecommapp.models import *

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

class ProductoViewSet(viewsets.ModelViewSet):
    
    def get_queryset(self):
        queryset = producto.objects.all()
        prodNom = self.request.query_params.get('nombre',None)
        prodId = self.request.query_params.get('id',None)
        if prodNom is not None:
            queryset = queryset.filter(nombre=prodNom)
        if prodId is not None:
            queryset = queryset.filter(id=prodId)
        if not queryset:
            ProductoSerializer.retrieve(self, queryset)
        return queryset

    serializer_class = ProductoSerializer

class CategoriaViewSet(viewsets.ModelViewSet):
    
    def get_queryset(self):
        #queryset = categoria.objects.all()
        queryset = categoria.objects.filter()
        if not queryset:
            CategoriaSerializer.retrieve(self, queryset)
        return queryset
    
    serializer_class = CategoriaSerializer

class CuponViewSet(viewsets.ModelViewSet):
    
    def get_queryset(self):
        queryset = cupon.objects.filter()
        serializer = CuponSerializer(queryset, many=True)
        cupCod = self.request.query_params.get('codigo',None)
        if cupCod is not None:
            queryset = queryset.filter(codigo=cupCod)
        if not queryset:
            CuponSerializer.retrieve(self, queryset)
        return queryset
    serializer_class = CuponSerializer

class ClienteViewSet(viewsets.ModelViewSet):
    
    queryset = cliente.objects.filter()
    serializer_class = ClienteSerializer

class PedidoViewSet(viewsets.ModelViewSet):
    
    def get_queryset(self):
        queryset = pedido.objects.all()
        clieId = self.request.query_params.get('cliente',None)
        if clieId is not None:
            queryset = queryset.filter(cliente=clieId)
        if not queryset:
            PedidoSerializer.retrieve(self, queryset)
        return queryset
    serializer_class = PedidoSerializer

class detallePedidoViewSet(viewsets.ModelViewSet):
    
    def get_queryset(self):
        queryset = detalle_pedido.objects.all()
        pedId = self.request.query_params.get('pedido',None)
        if pedId is not None:
            queryset = queryset.filter(pedido=pedId)
        return queryset
    def post(self, request):
        pedId = self.request.query_params.get('pedido',None)
        if pedId is not None:
            queryset = pedido.objects.all()
            queryset = queryset.filter(id=pedId)
        if not queryset:
            detallePedidoSerializer.validate(self, queryset)
        detallePedidoSerializer.save()
        return JsonResponse({"data": list(queryset), "error": False})
    serializer_class = detallePedidoSerializer

class estadoPedidoViewSet(viewsets.ModelViewSet):
    queryset = estado_pedido.objects.all()
    serializer_class = estadoPedidoSerializer

@csrf_exempt
def getPedido(request):
    queryset = pedido.objects.all().values()
    if request.method == 'POST':
        try:
            jsonData = json.loads(request.body)
            idPedido = int(jsonData["idPedido"])
            queryset = queryset.filter(id=idPedido)

            if queryset:
                querysetDet = detalle_pedido.objects.all().values()
                querysetDet = querysetDet.filter(pedido=idPedido)
            else:
                return JsonResponse({"data": "No existe Pedido", "error": True})
        except Exception as e:
            return JsonResponse({"data": e, "error": True})

    #return JsonResponse({"mensaje": "ok"})
    return JsonResponse({"pedido": list(queryset), "detalle": list(querysetDet), "error": False})

@csrf_exempt
def loginCliente(request):
    queryset = cliente.objects.all().values()
    if request.method == 'POST':
        try:
            jsonData = json.loads(request.body)
            cliUname = str(jsonData["username"])
            cliPass = str(jsonData["password"])
            if cliUname is not None:
                queryset = queryset.filter(username=cliUname, password=cliPass)
                if not queryset:
                    return JsonResponse({"data": "Credenciales incorrectas", "error": True})
        except Exception as e:
            return JsonResponse({"data": e, "error": True})

    return JsonResponse({"cliente": list(queryset), "error": False})
