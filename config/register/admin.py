from django.contrib import admin
from .models import User, UserProfile, SmsVerification  # Use correct model name

admin.site.register(User)
admin.site.register(UserProfile)
admin.site.register(SmsVerification)  # Corrected model name

