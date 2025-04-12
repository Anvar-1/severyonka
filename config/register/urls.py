from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenBlacklistView

urlpatterns = [
    path('register/', UserCreateView.as_view(), name='user-register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('check-user/', CheckUserView.as_view(), name='check-user'),
    # path('logout/', LogOutAPIView.as_view(), name='logout'),
    path('delete/<int:id>/', UserDeleteByIdView.as_view(), name='delete-user-by-id'),
    path('update/', UserUpdateView.as_view(), name='update'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('confirm-code/', VerifyCodeAPIView.as_view(), name='verify_code'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('change-user/', ChangeUserInformationView.as_view(), name='change-user'),
    path('token/blacklist/', TokenBlacklistView.as_view(), name='token_blacklist'),
        path('send_code/', SendCodeAPIView.as_view(), name='send_code'),
    path('verify-code/', VerifyCodeAPIView.as_view(), name='verify-code'),
    path('reset-password/', ResetPasswordAPIView.as_view(), name='reset-password'),
]