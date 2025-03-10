from django.db import models
from config.register.models import User


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    brand = models.CharField(max_length=50)
    title = models.CharField(max_length=50)
    created_at = models.DateTimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/images/', null=True, blank=True)
    category_id = models.ForeignKey('Category', related_name='products', on_delete=models.CASCADE)
    status = models.CharField(max_length=20,
                              choices=[('in_progress', 'Yigilyapti'), ('dispatched', 'Dostavka junatildi')],
                              default='in_progress')
    average_star = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    star_count = models.IntegerField(default=0)

    def update_star(self, star):
        """Yulduzlar reytingini yangilash."""
        total_stars = self.average_star * self.star_count
        self.star_count += 1
        new_average = (total_stars + star) / self.star_count
        self.average_star = new_average
        self.save()

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


class Discount(models.Model):
    product = models.ForeignKey(Product, related_name='discounts', on_delete=models.CASCADE)
    percentage = models.DecimalField(max_digits=5, decimal_places=2)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def __str__(self):
        return f'{self.percentage}% off on {self.product.name}'
