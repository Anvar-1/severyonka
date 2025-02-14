from rest_framework import serializers, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from . import views
from .models import User, UserProfile, SmsVerification
from django.contrib.auth.password_validation import validate_password
import requests
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'last_name', 'phone', 'password', 'role', 'birth_day', 'gender',
                  'region', 'populated_area', 'number_card', 'email']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])  # Parolni shifrlash
        user.save()
        return user


###################### sms kodni tekshirish ########################

class VerifyCodeSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=13)
    code = serializers.CharField(max_length=4)

    def validate(self, attrs):
        phone = attrs['phone']
        code = attrs['code']

        try:
            verification = SmsVerification.objects.get(user__phone=phone)
        except SmsVerification.DoesNotExist:
            raise serializers.ValidationError("SMS kodi topilmadi.")

        if not verification.is_code_valid(code):
            raise serializers.ValidationError("SMS kodi noto'g'ri yoki muddati o'tgan.")

        return attrs

    ####################### EDIT PROFILE ###################


class ChangeUserInformation(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password']

    def validate_username(self, username):
        if len(username) < 5 or len(username) > 30:
            raise ValidationError(
                {
                    "message": "Foydalanuvchi nomi 5 dan 30 gacha belgidan iborat bo'lishi kerak"
                }
            )
        if username.isdigit():
            raise ValidationError(
                {
                    "message": "Ushbu foydalanuvchi nomi butunlay raqamli"
                }
            )
        return username

    def update(self, instance, validated_data):

        instance.password = validated_data.get('password', instance.password)
        instance.username = validated_data.get('username', instance.username)
        if validated_data.get('password'):
            instance.set_password(validated_data.get('password'))

        instance.save()
        return instance

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['phone', 'password']


##################### reset-password ##########################

class PhoneSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=13)

    def validate_phone(self, value):
        if not value.isdigit() or len(value) < 9:
            raise serializers.ValidationError("Telefon raqam noto'g'ri formatda.")
        return value


class CodeSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=4)


class ResetPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(max_length=128)
    confirm_password = serializers.CharField(max_length=128)

    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError("Parollar mos kelmaydi.")
        return data
