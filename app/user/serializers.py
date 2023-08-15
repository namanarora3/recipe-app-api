'''serializers for the user API view'''

from django.contrib.auth import get_user_model, authenticate
# from django.utils.translation import gettext as _

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    '''serializer for the user object'''
    class Meta:
        model = get_user_model()
        fields = ['email', 'password', 'name']
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        '''create and return user with encrypted password'''
        # defauly behaviour is to create unencrypted, so we overwrite it
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        '''Update and return User'''
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data=validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class AuthTokenSerialiser(serializers.Serializer):
    """Serializer for the user auth token"""
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False,
    )

    def validate(self, attrs):
        user = authenticate(
          request=self.context.get('request'),
          email=attrs['email'],
          password=attrs['password']
        )

        if not user:
            msg = "Invalid input credentials"
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs
