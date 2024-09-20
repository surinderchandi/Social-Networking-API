import sys
from django.core.management.commands.runserver import Command as runserver
from django.core.management import execute_from_command_line

class Command(runserver):
    def handle(self, *args, **options):
        options['ssl_certificate'] = 'social_network/server.crt'
        options['ssl_key'] = 'social_network/server.key'
        super().handle(*args, **options)

if __name__ == "__main__":
    execute_from_command_line(sys.argv)
