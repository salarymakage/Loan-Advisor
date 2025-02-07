from django.contrib.auth.management.commands.createsuperuser import Command as BaseCommand
from django.core.management import CommandError
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Create a superuser with a phone number.'

    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument('--phone_number', required=True, help='Phone number for the superuser.')

    def handle(self, *args, **options):
        phone_number = options.get('phone_number')
        if not phone_number:
            raise CommandError('The --phone_number argument is required.')
        
        options['phone_number'] = phone_number
        super().handle(*args, **options)
