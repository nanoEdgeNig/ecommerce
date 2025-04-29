from .models import Category, Product, Review, Order, OrderItem
from django import forms

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['category_name', 'description']

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['product_name', 'price', 'description', 'stock', 'thumbnail', 'category']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['product', 'comment', 'rating']

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status']  

class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']
