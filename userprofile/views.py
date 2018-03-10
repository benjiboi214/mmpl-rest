from django.http import Http404, HttpResponse
from django.shortcuts import render
from rest_framework import permissions
from rest_framework.views import APIView

from userprofile.models import Profile


class MyProfileDetail(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get_player_object(self, user):
        obj, created = Profile.objects.get_or_create(user=user)
        if obj or created:
            return obj
        else:
            raise Http404

    def get(self, request, format=None):
        return HttpResponse("Here is your response testing goat!")

    def put(self, request, format=None):
        return HttpResponse("Here is your response testing goat!")
