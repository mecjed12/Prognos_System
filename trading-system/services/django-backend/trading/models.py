from django.db import models


class Forecast(models.Model):
    asset = models.CharField(max_length=20, db_index=True)
    horizon = models.CharField(max_length=10)  # z.B. "1h", "4h", "1d"
    prediction = models.FloatField()
    confidence = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)

    def __str__(self):
        return f"{self.asset} - {self.horizon} - {self.prediction} ({self.timestamp})"


class StrategyConfig(models.Model):
    key = models.CharField(max_length=50, unique=True)
    value = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.key}: {self.value}"
