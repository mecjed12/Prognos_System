from django.contrib import admin
from .models import Forecast, StrategyConfig


@admin.register(Forecast)
class ForecastAdmin(admin.ModelAdmin):
    list_display = ('asset', 'horizon', 'prediction', 'confidence', 'timestamp')
    list_filter = ('asset', 'horizon', 'timestamp')
    search_fields = ('asset',)
    ordering = ('-timestamp',)


@admin.register(StrategyConfig)
class StrategyConfigAdmin(admin.ModelAdmin):
    list_display = ('key', 'value')
    search_fields = ('key',)
