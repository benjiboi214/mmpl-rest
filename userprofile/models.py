from django.conf import settings
from django.contrib.auth import models as auth_models
from django.contrib.auth import get_user_model
from django.db import models as models


class Profile(models.Model):
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
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    address = models.CharField(max_length=200)
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

    class Meta:
        ordering = ('-created',)

    def __unicode__(self):
        return u'%s' % self.user.name

    def __str__(self):
        return self.user.name
