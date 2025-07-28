from django.urls import path
from . import views

urlpatterns = [
    path('forecasts/', views.ForecastListCreateView.as_view(), name='forecast-list-create'),
    path('strategy/config/', views.StrategyConfigListView.as_view(), name='strategy-config-list'),
    path('strategy/config/<str:key>/', views.StrategyConfigDetailView.as_view(), name='strategy-config-detail'),
    path('strategy/config/<str:key>/update/', views.StrategyConfigUpdateView.as_view(), name='strategy-config-update'),
]
