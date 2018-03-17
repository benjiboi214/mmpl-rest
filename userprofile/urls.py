from django.urls import include, path
from rest_framework import routers

from userprofile import views

# Need a 'me' url, requires auth and allows you to edit your own profile
# # Will be a custom implementation
# Need a set of readonly list and specific profiles
# # Can be done with the readonly viewset


urlpatterns = [path('players/me/',
                    views.MyProfileView.as_view(),
                    name='profile-me')]

router = routers.SimpleRouter()
router.register(r'players', views.ProfileViewSet)
urlpatterns += router.urls
