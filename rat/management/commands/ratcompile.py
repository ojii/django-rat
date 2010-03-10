from django.core.management.base import BaseCommand, CommandError
from django.core.management.commands.compilemessages import Command as CMCommand
from django.core.management import call_command
from django.conf import settings
from rat.utils import LazyLocalePaths

class Command(BaseCommand):
    """
    Compile the language files under RAT management.
    """
    option_list = CMCommand.option_list
    
    def handle(self, *args, **options):
        options['settings'] = settings.SETTINGS_MODULE
        if not hasattr(settings, 'LOCALE_PATHS') or not list(settings.LOCALE_PATHS):
            raise CommandError("ratcompile requires LOCALE_PATHS")
        if not isinstance(settings.LOCALE_PATHS, LazyLocalePaths):
            raise CommandError("ratcompile requires LOCALE_PATHS to be an instance of rat.utils.LazyLocalePaths")
        call_command('compilemessages', *args, **options)