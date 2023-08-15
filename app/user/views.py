"""Views for the user API"""
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework import permissions, authentication
from .serializers import UserSerializer, AuthTokenSerialiser
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings


class CreateUserView(CreateAPIView):  # name format is important
    """AUTH HEADER NOT REQD, Create a new user in the system"""  # docstring is important
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
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        '''Retrive and return the authenticated user'''
        user = self.request.user
        return user
