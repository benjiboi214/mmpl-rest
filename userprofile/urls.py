from django.urls import path, include
from userprofile import views

# Need a 'me' url, requires auth and allows you to edit your own profile
# # Will be a custom implementation
# Need a set of readonly list and specific profiles
# # Can be done with the readonly viewset

urlpatterns = [
    path('me/', views.player_me_detail, name='player_me_detail')
]