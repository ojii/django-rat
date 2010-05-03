from django.core.management.base import BaseCommand, CommandError
from django.core.management.commands.makemessages import Command as MMCommand
from django.core.exceptions import ImproperlyConfigured
from django.core.management import call_command
from path import path
import os    


class Command(BaseCommand):
    """
    Makemessages for all non-rat applications
    """
    option_list = MMCommand.option_list
    
    def handle(self, *args, **options):
        if args:
            raise CommandError("noratmake does not take any additional arguments")
        from django.conf import settings
        if not hasattr(settings, 'RAT_LOCALES_ROOT'):
            raise ImproperlyConfigured("noratmake requires the RAT_LOCALES_ROOT setting")
        self.locales_root = path(settings.RAT_LOCALES_ROOT)
        rat_apps = list(getattr(settings, 'RAT_APPS', settings.INSTALLED_APPS))
        if hasattr(settings, 'RAT_EXCLUDE_APPS'):
            for app in settings.RAT_EXCLUDE_APPS:
                if app in rat_apps:
                    rat_apps.remove(app)
        norat_apps = [app for app in settings.INSTALLED_APPS if app not in rat_apps]
        for app in norat_apps:
            print 'running makemessages in `%s`' % app
            self.handle_app(app, options)
        if hasattr(settings, 'RAT_SERVER_RESTART_COMMAND'):
            print 'restarting server'
            os.system(settings.RAT_SERVER_RESTART_COMMAND)
        print 'done'
            
    def handle_app(self, name, options):
        appdir = path(__import__(name).__file__).dirname()
        os.chdir(appdir) # so makemessages knows where to do it's magic
        try:
            call_command('makemessages', **options) # run it!
        except CommandError, e:
            print e.message
            return