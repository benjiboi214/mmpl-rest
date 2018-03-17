from django.http import Http404, HttpResponse
from django.shortcuts import render
from rest_framework import permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from userprofile.models import Profile
from userprofile.serializers import ProfileSerializer


class ProfileViewSet(viewsets.ModelViewSet):
    """
    A viewset that provides the standard actions
    """
    lookup_field = 'uuid'
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def get_permissions(self):
        """
        Instantiates and returns the list
        of permissions that this view requires.
        """
        if self.action == 'list':
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]


class MyProfileView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ProfileSerializer

    def get_player_object(self, user):
        obj, created = Profile.objects.get_or_create(user=user)
        if obj or created:
            return obj
        else:
            raise Http404

    def get(self, request, format=None):
        profile = self.get_player_object(request.user)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

    def put(self, request, format=None):
        profile = self.get_player_object(request.user)
        serializer = ProfileSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
