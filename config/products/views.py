import requests
from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from .models import Category, Product, Card, Comment, Order, Discount
from .serializers import CategorySerializer, ProductSerializer, CardSerializer, CommentSerializer, OrderSerializer, \
    DiscountSerializer, MyOderListSerializers
from rest_framework.response import Response
from .models import Card
from rest_framework.permissions import IsAuthenticated


class CategoryListCreateAPIView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductStarUpdateAPIView(APIView):
    def post(self, request, pk):
        product = Product.objects.filter(id=pk).first()
        if not product:
            return Response({"error": "Mahsulot topilmadi."}, status=status.HTTP_404_NOT_FOUND)

        star = request.data.get('star')
        if not star or star < 1 or star > 5:
            return Response({"error": "Yulduz 1 dan 5 gacha bo'lishi kerak."}, status=status.HTTP_400_BAD_REQUEST)

        # Yulduzni yangilash
        product.update_star(star)

        return Response({"message": "Yulduz muvaffaqiyatli qo'shildi.", "average_star": product.average_star},
                        status=status.HTTP_200_OK)

    def send_status_message(self, status, phone_number):
        messages = {
            'in_progress': "Mahsulot yigilyapti.",
            'dispatched': "Mahsulot dostavka junatildi.",
            'received': "Xaridorga berilgan",
            'not_received': "Mahsulot qabul qilinmadi.",
        }

        message = messages.get(status, "Holat aniqlanmadi.")

        self.send_sms(phone_number, message)

    def send_sms(self, phone_number, message):
        payload = {
            'to': phone_number,
            'message': message
        }

        response = requests.post('http://notify.eskiz.uz/api/message/sms/send', json=payload)

        if response.status_code == 200:
            print(f"SMS muvaffaqiyatli yuborildi: {message} - {phone_number}")
        else:
            print(f"SMS yuborishda xato: {response.text}")

    def notify_admin(self, product):
        admin_phone_number = '+998950038031'
        subject = "Mahsulot qabul qilinmadi"
        message = f"{product.name} mahsuloti qabul qilinmadi. Iltimos, nazorat qiling."

        self.send_sms(admin_phone_number, message)


class CardCreateView(generics.CreateAPIView):
    queryset = Card.objects.all()
    serializer_class = CardSerializer


class CardListView(generics.ListAPIView):
    serializer_class = CardSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Card.objects.filter(user=self.request.user)


class CommentListCreateView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CommentRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Comment.objects.filter(user=self.request.user)


class OrderCreateView(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    # permission_classes = [IsAuthenticated]


class DiscountCreateView(generics.CreateAPIView):
    queryset = Discount.objects.all()
    serializer_class = DiscountSerializer
    permission_classes = [IsAuthenticated]


class MyOrderListAPIView(ListAPIView):
    queryset = Order.objects.all()
    serializer_class = MyOderListSerializers

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Order.objects.filter(user=user)
        else:
            return Order.objects.none()


