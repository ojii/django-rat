from utils import LazyLocalePaths
from django.conf import settings

# LOCALE_PATHS *MUST* have AT LEAST the 'rat' locale paths!
setattr(settings._wrapped, 'LOCALE_PATHS', LazyLocalePaths(getattr(settings, 'LOCALE_PATHS', [])))