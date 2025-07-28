from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class Command(BaseCommand):
    help = 'Create auth token for a user'
    
    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='Username to create token for')
    
    def handle(self, *args, **options):
        username = options['username']
        try:
            user = User.objects.get(username=username)
            token, created = Token.objects.get_or_create(user=user)
            if created:
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Successfully created token for user {username}: {token.key}'
                    )
                )
            else:
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Token already exists for user {username}: {token.key}'
                    )
                )
        except User.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(
                    f'User {username} does not exist'
                )
            )
