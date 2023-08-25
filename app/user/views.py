"""Views for the user API"""
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.views import APIView
from rest_framework import permissions, authentication
from .serializers import UserSerializer, AuthTokenSerialiser, UserImageSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from rest_framework import viewsets, mixins

from rest_framework import status

from rest_framework.response import Response

from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiParameter,
    OpenApiTypes,
)


class CreateUserView(CreateAPIView):  # name format is important
    """
    AUTH HEADER NOT REQD, Create a new user in the system
    """  # docstring is important
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    '''AUTH HEADER NOT REQD, create a new auth token for the user'''
    # CUSTOM SERIALISER SO THAT WE CAN SHIFT FROM USERNAME TO EMAIL
    serializer_class = AuthTokenSerialiser
    # OPTIONAL- uses default, needed for browsable API
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(RetrieveUpdateAPIView):
    '''AUTH HEADER REQD, Manage the authenticated user'''
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        '''Retrive and return the authenticated user'''
        user = self.request.user
        return user


class ImageUpdateView(mixins.UpdateModelMixin, viewsets.GenericViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserImageSerializer

    def get_object(self):
        return self.request.user

    def perform_update(self, serializer):
        self.get_object().image.delete()
        return super().perform_update(serializer)


