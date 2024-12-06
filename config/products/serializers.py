from rest_framework import serializers
from .models import Category, Product, Card, Comment


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'brand', 'title', 'created_at', 'price', 'image', 'card_number', 'category_id']

class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = ['id', 'card_number']

    def validate_card_number(self, value):
        if len(value) < 16:
            raise serializers.ValidationError("Kartaning raqami 16 ta raqamdan kam bo'lmasligi kerak.")
        return value

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['user'] = request.user
        return super().create(validated_data)


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'product', 'user', 'created_at', 'text']
        read_only_fields = ['id', 'created_at']
