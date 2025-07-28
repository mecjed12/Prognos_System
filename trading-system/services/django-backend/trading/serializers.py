from rest_framework import serializers
from .models import Forecast, StrategyConfig

class ForecastSerializer(serializers.ModelSerializer):
    class Meta:
        model = Forecast
        fields = '__all__'
        read_only_fields = ('timestamp',)

class StrategyConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = StrategyConfig
        fields = '__all__'
