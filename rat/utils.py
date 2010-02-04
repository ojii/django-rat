from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from path import path

class LazyLocalePaths(list):
    def __iter__(self):
        return iter(self + get_locale_paths())


def get_locale_paths():
    """
    Return a list of paths to be put into LOCALE_PATHS.
    """
    if not hasattr(settings, 'RAT_LOCALES_ROOT'):
        raise ImproperlyConfigured("rat requires the RAT_LOCALES_ROOT setting")
    return [str(app.abspath()) for app in path(settings.RAT_LOCALES_ROOT).dirs()]