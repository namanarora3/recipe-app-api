"""Views for the user API"""
from rest_framework.generics import CreateAPIView
from .serializers import UserSerializer,AuthTokenSerialiser
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

class CreateUserView(CreateAPIView): # name format is important
    """Create a new user in the system""" # docstring is important
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    '''create a new auth token for the user'''
    # CUSTOM SERIALISER SO THAT WE CAN SHIFT FROM USERNAME TO EMAIL
    serializer_class = AuthTokenSerialiser
    # OPTIONAL- uses default, needed for browsable API
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
    


