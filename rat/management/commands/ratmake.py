from django.core.management.base import BaseCommand, CommandError
from django.core.management.commands.makemessages import Command as MMCommand
from django.core.exceptions import ImproperlyConfigured
from django.core.management import call_command
from optparse import make_option
from path import path
import os    


class Command(BaseCommand):
    """
    Do the RAT magic, move all translation files from the RAT_LOCALES_ROOT to the
    actual applications, run makemessages, move them back. 
    """
    option_list = MMCommand.option_list
    
    def handle(self, *args, **options):
        if args:
            raise CommandError("ratmake does not take any additional arguments")
        from django.conf import settings
        if not hasattr(settings, 'RAT_LOCALES_ROOT'):
            raise ImproperlyConfigured("ratmake requires the RAT_LOCALES_ROOT setting")
        self.locales_root = path(settings.RAT_LOCALES_ROOT)
        if not self.locales_root.isdir():
            self.locales_root.mkdir()
        rat_apps = list(getattr(settings, 'RAT_APPS', settings.INSTALLED_APPS))
        if hasattr(settings, 'RAT_EXCLUDE_APPS'):
            for app in settings.RAT_EXCLUDE_APPS:
                if app in rat_apps:
                    rat_apps.remove(app)
        for app in rat_apps:
            print 'rat making app `%s`' % app
            self.handle_app(app, options)
        if hasattr(settings, 'RAT_SERVER_RESTART_COMMAND'):
            print 'restarting server'
            os.system(settings.RAT_SERVER_RESTART_COMMAND)
        print 'done'
            
    def handle_app(self, name, options):
        appdir = path(__import__(name).__file__).dirname()
        localedir = appdir.joinpath('locale')
        if not localedir.isdir():
            print 'no locales found, ignoring'
            return # no locale, not interesting
        # remove 'new' language files
        for lang in localedir.dirs():
            po = lang.joinpath('LC_MESSAGES', 'django.po')
            mo = lang.joinpath('LC_MESSAGES', 'django.mo')
            if po.exists():
                po.remove()
            if mo.exists():
                mo.remove()
        # move 'old' language files
        rat_app = self.locales_root.joinpath(name)
        if not rat_app.exists():
            rat_app.mkdir()
        for lang in rat_app.dirs():
            app_lang_dir = localedir.joinpath(lang.basename())
            app_lc_dir = app_lang_dir.joinpath('LC_MESSAGES')
            if not app_lang_dir.exists():
                app_lang_dir.mkdir()
            if not app_lc_dir.exists():
                app_lc_dir.mkdir()
            po = lang.joinpath('LC_MESSAGES', 'django.po')
            mo = lang.joinpath('LC_MESSAGES', 'django.mo')
            if po.exists():
                po.move(app_lc_dir)
            if mo.exists():
                mo.move(app_lc_dir)
        # run makemessages for this app
        os.chdir(appdir) # so makemessages knows where to do it's magic
        try:
            call_command('makemessages', **options) # run it!
        except CommandError, e:
            print e.message
            return
        # move the 'made' language files back
        for lang in localedir.dirs():
            po = lang.joinpath('LC_MESSAGES', 'django.po')
            mo = lang.joinpath('LC_MESSAGES', 'django.mo')
            rat_lang_dir = rat_app.joinpath(lang.basename())
            rat_lc_dir = rat_lang_dir.joinpath('LC_MESSAGES')
            if not rat_lang_dir.exists():
                rat_lang_dir.mkdir()
            if not rat_lc_dir.exists():
                rat_lc_dir.mkdir()
            if po.exists():
                po.move(rat_lc_dir)
            if mo.exists():
                mo.move(rat_lc_dir)