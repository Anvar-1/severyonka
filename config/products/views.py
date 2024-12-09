from rest_framework import generics
from rest_framework.generics import ListAPIView

from .models import Category, Product, Comment, Order, Discount
from .serializers import CategorySerializer, ProductSerializer, CardSerializer, CommentSerializer, OrderSerializer, \
    DiscountSerializer, MyOderListSerializers
from .models import Card
from rest_framework.permissions import IsAuthenticated


class CategoryListCreateAPIView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


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
        # Faqatgina hozirgi foydalanuvchining buyurtmalarini qaytarish
        user = self.request.user
        return Order.objects.filter(user=user)


