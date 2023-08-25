"""Views for the user API"""
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.views import APIView
from rest_framework import permissions, authentication
from .serializers import UserSerializer, AuthTokenSerialiser, UserImageSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

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
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        '''Retrive and return the authenticated user'''
        user = self.request.user
        return user

# @extend_schema_view(

#     list=extend_schema(
#         parameters=[
#             OpenApiParameter(
#                 "tags",
#                 OpenApiTypes.STR,
#                 description="Comma sepersted list of IDs to filter"
#             ),
#             OpenApiParameter(
#                 "Ingredients",
#                 OpenApiTypes.STR,
#                 description="Comma seperated list if ingredients IDs to filter"
#             )
#         ]
#     )
# )
class ImageUpdateView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]


    def post(self, request):
        user = request.user
        serializer = UserImageSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
