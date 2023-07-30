# because of this directory structure django will automatically
# detect this as a management command, so this will run with manage.py
'''
django command to wait for db command
'''
import time
from django.core.management.base import BaseCommand
from django.db.utils import OperationalError
from psycopg2 import OperationalError as Psycopg2OpError


class Command(BaseCommand):
    "django command to wait for DB"

    def handle(self, *args, **options):
        self.stdout.write('Waiting for Database...')
        v = False
        while v is not True:
            try:
                self.check(databases=['default'])
                v = True
            except(Psycopg2OpError, OperationalError):
                self.stdout.write('DB not available, waiting for 1sec')
                time.sleep(1)
        self.stdout.write(self.style.SUCCESS('Connection Successful'))
