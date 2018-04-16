from django.conf import settings
from django.contrib.auth import models as auth_models
from django.contrib.auth import get_user_model
from django.db import models
from utils.models import TimeStampedUuidModel


class Profile(TimeStampedUuidModel):

    # Choices
    UMPIRE_ACCREDITATION_CHOICES = (
        ('N', 'None'),
        ('A', 'A Grade'),
        ('B', 'B Grade'),
        ('C', 'C Grade'),
        ('D', 'D Grade'),
        ('E', 'E Grade')
    )

    # Fields
    name = models.CharField(
        max_length=255,
        blank=True)
    address = models.CharField(
        max_length=200,
        blank=True)
    phone_number = models.CharField(
        max_length=30,
        blank=True)
    date_of_birth = models.DateField(null=True)
    umpire_accreditation = models.CharField(
        max_length=1,
        choices=UMPIRE_ACCREDITATION_CHOICES,
        default='N')

    # Relationship Fields
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="profile")

    def __unicode__(self):
        return u'%s' % self.name

    def __str__(self):
        return self.name


class Claim(TimeStampedUuidModel):

    # Fields
    id_code = models.CharField(
        max_length=20,
        blank=True
    )

    # Relationship Fields
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile_claim"
    )
    profile = models.OneToOneField(
        Profile,
        on_delete=models.CASCADE,
        related_name="claim"
    )

    # Model Methods (Business Logic)
    def reject_claim(self):
        pass

    def accept_claim(self):
        pass

    # Helper Methods
    def __unicode__(self):
        return u'%s' % self.user.name

    def __str__(self):
        return self.user.name