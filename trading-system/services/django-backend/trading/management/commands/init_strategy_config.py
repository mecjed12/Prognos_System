from django.core.management.base import BaseCommand
from trading.models import StrategyConfig


class Command(BaseCommand):
    help = 'Initialize default strategy configuration'

    def handle(self, *args, **options):
        # Default strategy configuration
        defaults = [
            {'key': 'risk_factor', 'value': '1.0'},
            {'key': 'position_size_limit', 'value': '0.1'},
            {'key': 'confidence_threshold', 'value': '0.7'},
            {'key': 'max_drawdown_limit', 'value': '0.05'},
            {'key': 'volatility_multiplier', 'value': '1.0'},
        ]

        for config in defaults:
            obj, created = StrategyConfig.objects.get_or_create(
                key=config['key'],
                defaults={'value': config['value']}
            )
            
            if created:
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Created {config["key"]} = {config["value"]}'
                    )
                )
            else:
                self.stdout.write(
                    f'Already exists: {config["key"]} = {obj.value}'
                )

        self.stdout.write(
            self.style.SUCCESS('Successfully initialized strategy configuration')
        )
