from authtools.models import AbstractNamedUser, UserManager
from django.utils.translation import ugettext_lazy as _

from userprofile.models import Profile


class UserManager(UserManager):

    def create_user(self, email, password=None, **kwargs):
        user = super(UserManager, self).create_user(email, password, **kwargs)
        profile = Profile.objects.create(user=user)
        profile.save()
        return user


class User(AbstractNamedUser):
    objects = UserManager()

    class Meta(AbstractNamedUser.Meta):
        swappable = 'AUTH_USER_MODEL'
        verbose_name = _('user')
        verbose_name_plural = _('users')
