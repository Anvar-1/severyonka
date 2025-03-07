from rest_framework import serializers, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from . import views
import random
from .models import User, UserProfile, SmsVerification
from django.contrib.auth.password_validation import validate_password
import requests
from django.contrib.auth import get_user_model
from phonenumber_field.modelfields import PhoneNumberField

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

class SendCodeSerializer(serializers.Serializer):
    phone = serializers.CharField(required=True)

    def send_verification_code(self, phone):
        code = "".join([str(random.randint(0, 9)) for _ in range(4)])

        url = "http://notify.eskiz.uz/api/auth/login"

        payload = {'email': 'imronhoja336@mail.ru',
                   'password': 'ombeUIUC8szPawGi3TXgCjDXDD0uAIx2AmwLlX9M'}
        files = [

        ]
        headers = {
            # 'Authorization': f"{Bearer}"
        }

        response = requests.request("POST", url, headers=headers, data=payload, files=files)

        token1 = response.json()["data"]["token"]

        url = "http://notify.eskiz.uz/api/message/sms/send"

        payload = {'mobile_phone': str(phone),
                   'message': f"Envoy ilovasiga ro‘yxatdan o‘tish uchun tasdiqlash kodi: {code}",
                   'from': '4546',
                   'callback_url': 'http://0000.uz/test.php'}
        files = [

        ]

        headers = {
            'Authorization': f"Bearer {token1}"
        }

        response = requests.request("POST", url, headers=headers, data=payload, files=files)
        print(code)
        return code


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