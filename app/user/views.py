"""Views for the user API"""
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.views import APIView
from rest_framework import permissions, authentication
from .serializers import (
    UserSerializer,
    AuthTokenSerialiser,
    UserImageSerializer,
    ChangePasswordSerializer,
    ResetPasswordSerializer,
    generateOTPSerializer
)
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from rest_framework import viewsets, mixins

from rest_framework import status

from rest_framework.response import Response

from django.contrib.auth import get_user_model

import random, math

from user.email import send

from core.models import ResetPassword

from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiParameter,
    OpenApiTypes,
)

def createOTP():
    digits = "0123456789"
    OTP = ""
    for i in range(4) :
        OTP += digits[math.floor(random.random() * 10)]
    return OTP

def send_email(otp, email):
    url = "http://127.0.0.1:8000/api/user/reset_password/?email="+email+"&otp="+otp

    msg = "please clink on the URL for setting your password- "+ url
    send(
        "Password Reset OTP from Recipe APP",
        msg,
        [email]
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

class ChangePasswordView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        # print(serializer.data)
        if(serializer.is_valid()):
            user = request.user
            if user.check_password(serializer.data.get('old_password')):
                user.set_password(serializer.data.get('new_password2'))
                user.save()
                return Response({"message": "Password updated successfully"}, status=status.HTTP_200_OK)
            return Response({'error': "Old password incorrect"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def get(self, request):
        return Response({"message": "Change your password here"})


class ResetPasswordGenerateToken(APIView):
    serializer_class = generateOTPSerializer

    def post(self, request):
        email = request.data.get('email')
        try:
            user = get_user_model().objects.get(email=email)
        except:
            user = None
        if user is None:
            return Response({"error": "User with email not found"}, status=status.HTTP_400_BAD_REQUEST)
        token, created = ResetPassword.objects.get_or_create(
            user=user
        )
        OTP = createOTP()
        setattr(token, 'otp', OTP)
        token.save()
        try:
            send_email(OTP, email)
        except:
            Response({"error": "Unable to send OTP, please try again!"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "email sent successfully"}, status=status.HTTP_200_OK)

class ResetPasswordView(APIView):
    serializer_class = ResetPasswordSerializer

    def post(self, request):
        email = request.query_params.get('email', None)
        otp = request.query_params.get('otp', None)
        if email is None or otp is None:
            return Response({'error': "Invalid URL"}, status=status.HTTP_404_NOT_FOUND)
        serializer = ResetPasswordSerializer(data=request.data)
        # print(serializer.data)
        if(serializer.is_valid()):
            try:
                # user = get_user_model().objects.get(email=serializer.data.get('email'))
                user = get_user_model().objects.get(email=email)
            except:
                return Response({'error': "email not recognised"}, status=status.HTTP_400_BAD_REQUEST)
            try:
                # token = ResetPassword.objects.get(user=user, otp=serializer.data.get('token'))
                token = ResetPassword.objects.get(user=user, otp=otp)
            except:
                return Response({'error': "email or OTP incorrect, please try again!"}, status=status.HTTP_400_BAD_REQUEST)
            if token is not None:
                user.set_password(serializer.data.get('new_password2'))
                user.save()
                setattr(token, 'otp', '0')
                token.save()
                return Response({"message": "Password updated successfully"}, status=status.HTTP_200_OK)
            return Response({'error': "email or OTP incorrect"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

