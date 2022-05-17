from django.utils.decorators import method_decorator

from rest_framework import permissions, status
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.decorators import action
from rest_framework.response import Response

from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema

from apps.helpers.viewsets import ExtendedModelViewSet
from apps.chemical_resistance_calc.models import TableOfChemicalResistance
from .serializers import (
    TableOfChemicalResistanceSerializer, EnvironmentSerializer,
    CalcStateRequestSerializer, CalcStateResponseSerializer,
    CalcConcentrateRequestSerializer, CalcConcentrateResponseSerializer,
    CalcTemperatureRequestSerializer, CalcTemperatureResponseSerializer,
    CalcResultRequestSerializer, CalcResultResponseSerializer,
    CalculateCalculatorRequestRequestSerializer,
    CalculateCalculatorRequestResponseSerializer,
)
from .filters import TableOfChemicalResistanceFilter
from apps.helpers.exceptions import ErrorResponseSerializer


@method_decorator(
    name='list',
    decorator=swagger_auto_schema(responses={400: ErrorResponseSerializer})
)
class ChemicalResistanceCalcViewSet(ExtendedModelViewSet):
    queryset = TableOfChemicalResistance.objects.all()
    serializer_class = TableOfChemicalResistanceSerializer
    permission_classes = (permissions.AllowAny,)
    filter_class = TableOfChemicalResistanceFilter
    filter_backends = (DjangoFilterBackend, OrderingFilter)

    @swagger_auto_schema(responses={status.HTTP_200_OK: EnvironmentSerializer})
    @action(methods=['get'], detail=False, url_path='environment', url_name='environment')
    def environment(self, request):
        qs = self.filter_queryset(self.get_queryset()).distinct('name').values('id', 'name', 'formula')
        serializer = EnvironmentSerializer(qs, many=True)
        page = self.paginate_queryset(serializer.data)
        if page:
            return self.get_paginated_response(page)
        return Response(serializer.data)

    @swagger_auto_schema(responses={status.HTTP_200_OK: CalcStateResponseSerializer})
    @action(methods=['get'], detail=False, url_path='state', url_name='state')
    def state(self, request):
        serializer = CalcStateRequestSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        qs = self.get_queryset().filter(
            name=serializer.data['environment']
        ).distinct('state').values('id', 'name', 'formula', 'state',)

        serializer = CalcStateResponseSerializer(qs, many=True)
        page = self.paginate_queryset(serializer.data)
        if page:
            return self.get_paginated_response(page)
        return Response(serializer.data)

    @swagger_auto_schema(responses={status.HTTP_200_OK: CalcConcentrateResponseSerializer})
    @action(methods=['get'], detail=False, url_path='concentration', url_name='concentration')
    def concentration(self, request):
        serializer = CalcConcentrateRequestSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        qs = self.get_queryset().filter(
            name=serializer.data['environment'],
            state=serializer.data['state'],
        ).distinct('concentration').values('id', 'concentration',)

        serializer = CalcConcentrateResponseSerializer(qs, many=True)
        page = self.paginate_queryset(serializer.data)
        if page:
            return self.get_paginated_response(page)
        return Response(serializer.data)

    @swagger_auto_schema(responses={status.HTTP_200_OK: CalcTemperatureResponseSerializer})
    @action(methods=['get'], detail=False, url_path='temperature', url_name='temperature')
    def temperature(self, request):
        serializer = CalcTemperatureRequestSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        qs = self.get_queryset().filter(
            name=serializer.data['environment'],
            state=serializer.data['state'],
            concentration=serializer.data['concentration'],
        ).distinct('temperature').values('id', 'temperature',)

        serializer = CalcTemperatureResponseSerializer(qs, many=True)
        page = self.paginate_queryset(serializer.data)
        if page:
            return self.get_paginated_response(page)
        return Response(serializer.data)

    @swagger_auto_schema(responses={status.HTTP_200_OK: CalcResultResponseSerializer})
    @action(methods=['get'], detail=False, url_path='result', url_name='result')
    def result(self, request):
        serializer = CalcResultRequestSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        # Всегда ожидается один объект (это следует из таблицы). Если
        # что-то в логике таблицы/калькулятора поменяется - будет ошибка.
        # На время разметил first(), есть неточности в таблице хим. соединений.
        qs = self.get_queryset().filter(
            name=serializer.data['environment'],
            state=serializer.data['state'],
            concentration=serializer.data['concentration'],
            temperature=serializer.data['temperature'],
        ).first()

        serializer = CalcResultResponseSerializer(qs)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=CalculateCalculatorRequestRequestSerializer,
        responses={
            status.HTTP_200_OK: CalculateCalculatorRequestResponseSerializer})
    @action(methods=['post'], detail=False, url_path='send-calc-request', url_name='send-calc-request')
    def send_calc_result(self, request):
        serializer = CalculateCalculatorRequestRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        obj = serializer.save()
        serializer = CalculateCalculatorRequestResponseSerializer(obj)
        return Response(serializer.data)
