#because of this directory structure django will automatically detect this as a management command, so this will run with manage.py
'''
django command to wait for db command
'''

from django.core.management.base import BaseCommand

class Command(BaseCommand):
    "django command to wait for DB"

    def handle(self,*args,**options):
        pass