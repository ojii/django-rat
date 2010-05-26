from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ImproperlyConfigured
from django.core.management import call_command
from path import path
import os    


class Command(BaseCommand):
    """
    Delete all duplicate files (from the app locales) which exist both in rat
    locales and in the app locales.
    """
    
    def handle(self, *args, **options):
        raise NotImplemented
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
        rat_app = self.locales_root.joinpath(name, 'locale')
        if not rat_app.exists():
            self.init_app(localedir, rat_app, name)
        # remove 'new' language files ( egg -> void )
        for lang in localedir.dirs():
            po = lang.joinpath('LC_MESSAGES', 'django.po')
            mo = lang.joinpath('LC_MESSAGES', 'django.mo')
            # check if we have this locale in rat
            if rat_app.joinpath(lang, 'LC_MESSAGES', 'django.po').exists():
                if po.exists():
                    po.remove()
                if mo.exists():
                    mo.remove()
                
    def init_app(self, localedir, rat_app, name):
        """
        Initialize an app for ratting. This means we copy the current language
        files from the egg into rat
        """
        for lang in localedir.dirs():
            po = lang.joinpath('LC_MESSAGES', 'django.po')
            mo = lang.joinpath('LC_MESSAGES', 'django.mo')
            rat_lc_dir = rat_app.joinpath(lang.basename(), 'LC_MESSAGES')
            if not rat_lc_dir.exists():
                rat_lc_dir.makedirs()
            if po.exists():
                po.move(rat_lc_dir)
            if mo.exists():
                mo.move(rat_lc_dir)
