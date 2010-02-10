from django.core.management.base import BaseCommand, CommandError
from django.core.management.commands.makemessages import Command as MMCommand
from django.core.management import call_command
import os    


class Command(BaseCommand):
    """
    Do the RAT magic, move all translation files from the RAT_LOCALES_ROOT to the
    actual applications, run makemessages, move them back. 
    
    You can use your standard makemessages arguments (--extension,...) for this
    command.
    """
    option_list = MMCommand.option_list
    
    def handle(self, *args, **options):
        if args:
            raise CommandError("makeallmessages does not take any additional arguments")
        from django.conf import settings
        for app in settings.INSTALLED_APPS:
            # ignore django core apps
            if app.startswith('django.'):
                continue
            self.handle_app(app, options)
        print 'done'
            
    def handle_app(self, name, options):
        appdir = os.path.dirname((__import__(name).__file__))
        if not os.path.exists(os.path.join(appdir, 'locale')):
            print 'no locales in %s, ignoring...' % name
            return
        print 'making messages for %s...' % name
        # run makemessages for this app
        os.chdir(appdir) # so makemessages knows where to do it's magic
        try:
            call_command('makemessages', **options) # run it!
        except CommandError, e:
            print e.message
            return