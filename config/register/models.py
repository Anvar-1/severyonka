import random
from django.db import models
from django.contrib.auth.models import AbstractUser
from rest_framework_simplejwt.tokens import RefreshToken


class User(AbstractUser):
    phone = models.CharField(max_length=15, unique=True, help_text="+998950701662")
    number_card = models.CharField(max_length=30, unique=True)
    email = models.EmailField(unique=True)
    birth_day = models.CharField(max_length=30, help_text="kun.oy.yil (01.06.2004)")
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female')])
    region = models.CharField(max_length=100)
    populated_area = models.CharField(max_length=100)
    confirm_password = models.CharField(max_length=128, default=False)
    code = models.CharField(max_length=4, null=True, blank=True)
    is_confirmed = models.BooleanField(default=False)

    def create_verify_code(self):
        # Telefon raqamidan foydalanib tasdiqlash kodi yaratish
        code = "".join([str(random.randint(0, 10000) % 10) for _ in range(4)])
        self.code = code  # User modelidagi `code` maydoniga yozish
        self.save()  # Yangi kodni saqlash
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
    REQUIRED_FIELDS = ['username', 'email', 'number_card', 'birth_day', 'gender', 'region', 'populated_area']

    def __str__(self):
        return self.phone

