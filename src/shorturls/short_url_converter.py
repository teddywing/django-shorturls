import urlparse
from django.conf import settings
from django.core import urlresolvers
from shorturls import default_converter as converter


class ShortURLConverter(object):
    def __init__(self, obj):
        self.obj = obj

    def shorten(self):
        try:
            prefix = self.get_prefix(self.obj)
        except (AttributeError, KeyError):
            return ''

        tinyid = converter.from_decimal(self.obj.pk)

        if hasattr(settings, 'SHORT_BASE_URL') and settings.SHORT_BASE_URL:
            return urlparse.urljoin(settings.SHORT_BASE_URL, prefix+tinyid)

        try:
            return urlresolvers.reverse('shorturls.views.redirect', kwargs={
                'prefix': prefix,
                'tiny': tinyid
            })
        except urlresolvers.NoReverseMatch:
            return ''

    def get_prefix(self, model):
        if not hasattr(self.__class__, '_prefixmap'):
            self.__class__._prefixmap = dict(
                (m, p) for p, m in settings.SHORTEN_MODELS.items())
        key = '%s.%s' % (
            model._meta.app_label,
            model.__class__.__name__.lower())
        return self.__class__._prefixmap[key]
