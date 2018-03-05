from authtools.models import AbstractNamedUser
from django.utils.translation import ugettext_lazy as _


class User(AbstractNamedUser):
    class Meta(AbstractNamedUser.Meta):
        swappable = 'AUTH_USER_MODEL'
        verbose_name = _('user')
        verbose_name_plural = _('users')
