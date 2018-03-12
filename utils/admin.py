from authtools.admin import NamedUserAdmin
from django.contrib import admin

from utils.models import User

admin.site.register(User, NamedUserAdmin)
