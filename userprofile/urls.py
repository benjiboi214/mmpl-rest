from django.urls import include, path

from userprofile import views

# Need a 'me' url, requires auth and allows you to edit your own profile
# # Will be a custom implementation
# Need a set of readonly list and specific profiles
# # Can be done with the readonly viewset


urlpatterns = [
    path(
        'players/',
        views.ProfileList.as_view(),
        name='profile-list'
    ),
    path(
        'players/me/',
        views.ProfileMe.as_view(),
        name='profile-me'
    ),
    path(
        'players/claims/',
        views.ClaimList.as_view(),
        name='claim-list'
    ),
    path(
        'players/<uuid>/',
        views.ProfileDetail.as_view(),
        name='profile-detail'
    )
]
