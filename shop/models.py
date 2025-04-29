from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
      category_name = models.CharField(max_length=50)
      thumbnail = models.ImageField(upload_to='category_images/', blank=True, null=True)
      description = models.TextField()
      
      def __str__(self):
          return self.category_name


class Product(models.Model):
    product_name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    stock = models.IntegerField(default=1)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    thumbnail = models.ImageField(upload_to='product_images/')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_product')
    
    def __str__(self):
          return self.product_name

class Order(models.Model):
    STATUS_OPTIONS = [
        ('PENDING', 'Pending'),
        ('DELIVERED', 'Delivered'),
        ('CANCELED', 'Canceled'),
    ]

    ordered_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ordered_by')
    ordered_on = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_OPTIONS)

    def __str__(self):
        return f'Order #{self.pk} by {self.ordered_by.username}'

    def total_amount(self):
        return sum(item.subtotal() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def subtotal(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f'{self.quantity} x {self.product.product_name} (Order #{self.order.id})'



class Review(models.Model):
    RATING_OPTIONS = [
        (1, 'Very Poor'),
        (2, 'Poor'),
        (3, 'Good'),
        (4, 'Very Good'),
        (5, 'Excellent'),
    ]
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_review')
    comment = models.TextField()
    rating = models.CharField(max_length=1, choices=RATING_OPTIONS)
    reviewed_on = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return f'Review by {self.reviewer.username}: {self.comment}'
    
    
