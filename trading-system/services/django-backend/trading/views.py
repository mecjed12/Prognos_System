from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Forecast, StrategyConfig
from .serializers import ForecastSerializer, StrategyConfigSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter


class ForecastListCreateView(generics.ListCreateAPIView):
    queryset = Forecast.objects.all()
    serializer_class = ForecastSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['asset', 'horizon']
    ordering_fields = ['timestamp']
    ordering = ['-timestamp']


class StrategyConfigListView(generics.ListAPIView):
    queryset = StrategyConfig.objects.all()
    serializer_class = StrategyConfigSerializer


class StrategyConfigUpdateView(generics.UpdateAPIView):
    queryset = StrategyConfig.objects.all()
    serializer_class = StrategyConfigSerializer
    lookup_field = 'key'


class StrategyConfigDetailView(generics.RetrieveAPIView):
    queryset = StrategyConfig.objects.all()
    serializer_class = StrategyConfigSerializer
    lookup_field = 'key'
