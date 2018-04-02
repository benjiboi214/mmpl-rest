from django.http import Http404, HttpResponse
from django.shortcuts import render
from rest_framework import permissions, status, viewsets, generics, mixins
from rest_framework.response import Response
from rest_framework.views import APIView

from userprofile.models import Profile
from userprofile.serializers import ProfileSerializer
from utils import permissions as custom_permissions


class ProfileList(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (custom_permissions.IsAdminOrReadOnly,)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class ProfileDetail(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (
        custom_permissions.IsAdminOrReadOnly,
        custom_permissions.IsAuthenticatedAndProfileOwnerOrReadOnly,
    )
    lookup_field = 'uuid'

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class ProfileMe(APIView):
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
