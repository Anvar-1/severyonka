import random
from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumbers import timezone
from rest_framework_simplejwt.tokens import RefreshToken

ORDIRNARY_USER, MANAGER, ADMIN = ('ordinary user', 'manager', 'admin')

class User(AbstractUser):
    phone = models.CharField(max_length=13, unique=True, null=True, blank=True)
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
    code = models.CharField(max_length=4, null=True, blank=True)
    is_confirmed = models.BooleanField(default=False)
    number_card = models.CharField(max_length=16, null=True, blank=True)
    email = models.EmailField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.username

    def create_verify_code(self):
        self.code = "".join([str(random.randint(0, 9)) for _ in range(4)])  # 4 raqamli kod
        self.save()
        return self.code

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
        return self.phone


class SmsVerification(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=4)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_code_valid(self, code):
        if self.code == code and (timezone.now() - self.created_at).seconds < 60:
            return True
        return False


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=13, unique=True, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.user.name

