import uuid as uuid_lib

from authtools.models import AbstractNamedUser, UserManager
from django.db import models
from django.utils.translation import ugettext_lazy as _


class TimeStampedUuidModel(models.Model):

    # Fields
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    uuid = models.UUIDField(
        db_index=True,
        default=uuid_lib.uuid4,
        editable=False
    )

    class Meta:
        abstract = True
        ordering = ('-created',)


class CustomUserManager(UserManager):

    def create_user(self, email, password=None, **kwargs):
        from userprofile.models import Profile

        user = super(CustomUserManager, self).create_user(
            email, password, **kwargs)
        profile = Profile.objects.create(user=user)
        profile.save()
        return user


class User(AbstractNamedUser):
    objects = CustomUserManager()

    class Meta(AbstractNamedUser.Meta):
        swappable = 'AUTH_USER_MODEL'
        verbose_name = _('user')
        verbose_name_plural = _('users')
