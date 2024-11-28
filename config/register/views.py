from django.contrib.auth import user_logged_in, authenticate, login
from django.contrib.auth.hashers import check_password
from rest_framework.exceptions import ValidationError
from rest_framework.generics import UpdateAPIView, CreateAPIView
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from .models import User
from .serializers import UserSerializer, ChangeUserInformation, LogoutSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import generics, permissions, status
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from .serializers import UserSerializer

User = get_user_model()


class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})


class LoginAPIView(APIView):
    def post(self, request):
        data = request.data
        user = User.objects.filter(phone=data['phone']).first()
        if not user:
            return Response({'message': 'Bunday foydalanuvchi topilmadi!'}, status=status.HTTP_404_NOT_FOUND)

        if check_password(data['password'], user.password):
            return Response({'token': user.token()['access'], "message": 'Yahhooo'}, status=status.HTTP_200_OK)
        print("Passwordjon", data['password'])
        print("Phonejon", data['phone'])

        return Response({'error': 'Parolingiz xato'}, status=status.HTTP_400_BAD_REQUEST)


class LogOutAPIView(APIView):
    serializer_class = LogoutSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        try:
            refresh_token = self.request.data['refresh']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'success': True, 'message': "Muvaffaqiyatli hisobingizdan chiqdingiz!"}, status=205)
        except TokenError:
            return Response(status=400)

class UserDeleteView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = User.objects.all()

    def delete(self, request, *args, **kwargs):
        user = self.get_object()
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserUpdateView(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def put(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyCodeAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        user = self.request.user
        code = self.request.data.get('code')
        self.check_verify(user, code)

        return Response(
            data={
                "success": True,
                "access": user.token()['access'],
                "refresh": user.token()['refresh']
            }
        )

    @staticmethod
    def check_verify(user, code):
        # Code va telefon raqami orqali tekshirish
        verifies = User.objects.filter(code=code, phone=user.phone, is_confirmed=False)
        print("Verifies queryset: ", verifies)
        print("Phone", user.phone)
        print("Code", user.code)

        if not verifies.exists():
            data = {
                "message": "Tasdiqlash kodingiz xato yoki eskirgan"
            }
            raise ValidationError(data)
        else:
            # Kod to'g'ri bo'lsa, tasdiqlashni yangilaymiz
            user.save()
        if user.is_confirmed == False:
            verifies.update(is_confirmed=True)
            return  verifies
        return True


####################  EDIT PROFILE #################

class ChangeUserInformationView(UpdateAPIView):
    # permission_classes = [IsAuthenticated, ]
    serializer_class = ChangeUserInformation
    http_method_names = ['patch', 'put']

    def get_object(self):
        if not self.request.user.is_authenticated:
            raise AuthenticationFailed('Foydalanuvchi autentifikatsiya qilinmagan')
        return self.request.user

    def update(self, request, *args, **kwargs):
        super(ChangeUserInformationView, self).update(request, *args, **kwargs)
        data = {
            'success': True,
            "message": "Foydalanuvchi muvaffaqiyatli yangilandi",
        }
        return Response(data, status=200)

    def partial_update(self, request, *args, **kwargs):
        super(ChangeUserInformationView, self).partial_update(request, *args, **kwargs)
        data = {
            'success': True,
            "message": "Foydalanuvchi muvaffaqiyatli yangilandi",
            'auth_status': self.request.user.auth_status,
        }
        return Response(data, status=200)












