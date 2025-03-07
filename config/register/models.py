import random
from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumbers import timezone
from rest_framework_simplejwt.tokens import RefreshToken
from phonenumber_field.modelfields import PhoneNumberField

ORDIRNARY_USER, MANAGER, ADMIN = ('ordinary user', 'manager', 'admin')


class User(AbstractUser):
    phone = PhoneNumberField(unique=True, null=True, blank=True)
    ROLE_CHOICES = (
        (ORDIRNARY_USER, ORDIRNARY_USER),
        (MANAGER, MANAGER),
        (ADMIN, ADMIN)
    )
    role = models.CharField(max_length=15, choices=ROLE_CHOICES, default=ORDIRNARY_USER)
    birth_day = models.CharField(max_length=15, help_text="kun.oy.yil (01.06.2004)")
    gender = models.CharField(max_length=10)
    region = models.CharField(max_length=100)
    populated_area = models.CharField(max_length=100)
    number_card = models.CharField(max_length=16, null=True, blank=True)
    email = models.EmailField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.username

    def create_verify_code(self):
        code = "".join([str(random.randint(0, 9)) for _ in range(4)])
        SmsVerification.objects.create(
            phone=str(self.phone),
            code=code
        )
        return code

    def hashing_password(self):
        if not self.password.startswith('pbkdf2_sha256'):
            self.set_password(self.password)

    def save(self, *args, **kwargs):
        self.clean()
        super(User, self).save(*args, **kwargs)

    def clean(self):
        self.hashing_password()

    def token(self):
        refresh = RefreshToken.for_user(self)
        return {
            "access": str(refresh.access_token),
            "refresh": str(refresh)
        }

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['username', 'email', 'number_card', 'birth_day', 'gender', 'region', 'role', 'populated_area']

    def __str__(self):
        return str(self.phone)


class SmsVerification(models.Model):
    phone = PhoneNumberField(unique=True)
    code = models.CharField(max_length=4)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.phone} - {self.code}"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=13, unique=True, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.user.name

