from django.db import models
from config.register.models import User


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Discount(models.Model):
    product = models.ForeignKey('Product', related_name='discounts', on_delete=models.CASCADE)
    percentage = models.DecimalField(max_digits=5, decimal_places=2)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    status = models.BooleanField(default=False)
    case = models.CharField(max_length=255)
    total_percentage = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f'{self.percentage}% off on {self.product.name}'

    def get_discounted_price(self):
        original_price = self.product.price
        percentage = self.percentage  # 'self.percentage' ni ishlatish kerak
        total = original_price - (original_price * percentage / 100)
        return total

    def clean(self):
        # Get discounted price and assign it to total_percentage
        self.total_percentage = self.get_discounted_price()

    def save(self, *args, **kwargs):
        self.clean()
        super(Discount, self).save(*args, **kwargs)


class Product(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    cash_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    card_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    description = models.TextField()
    additional_info = models.TextField(blank=True, null=True)
    rating = models.PositiveIntegerField(default=5)
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, models.CASCADE, null=True, blank=True)
    discount = models.ForeignKey('Discount', on_delete=models.CASCADE, related_name='discounts', null=True, blank=True)

    def __str__(self):
        return self.name


class Card(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cards')
    card_number = models.CharField(max_length=16)

    def __str__(self):
        return f"{self.user.username} - {self.card_number}"


class Comment(models.Model):
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    comment = models.TextField()

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Comment by {self.user} on {self.product}"


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='products')
    address = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Order {self.id} by {self.user.name}'
