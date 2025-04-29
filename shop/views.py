from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import (
    TemplateView, CreateView, ListView, 
    DetailView, UpdateView, DeleteView, View
    )
from .models import Category, Product, Order, OrderItem, Review
from .forms import CategoryForm, ProductForm, ReviewForm, OrderForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.utils import timezone


class IndexView(ListView):
    model = Product
    template_name = 'index.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.request.GET.get('q', '').strip()

        if q:
            queryset = queryset.filter(product_name__icontains=q)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['reviews'] = Review.objects.all()
        context['is_paginated'] = context['page_obj'].has_other_pages()
        return context
    
class DashboardIndexView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard_index.html'
    
class AboutView(TemplateView):
    template_name = 'about.html'
    
class ContactView(TemplateView):
    template_name = 'contact.html'
    
# Categories
class CategoryListView(ListView):
    model = Category
    template_name = 'shop/category/category_list.html'
    context_object_name = 'categories'
    

class CategoryCreateView(CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'shop/category/category_create.html'
    success_url = reverse_lazy('shop:category_list')

class CategoryUpdateView(UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'shop/category/category_update.html'
    success_url = reverse_lazy('shop:category_list')

class CategoryDetailView(DetailView):
    model = Category
    template_name = 'shop/category/category_detail.html'

class CategoryDeleteView(DeleteView):
    model = Category
    template_name = 'shop/category/category_delete.html'
    success_url = reverse_lazy('shop:category_list')
    

# Products
class ProductListView(ListView):
    model = Product
    template_name = 'shop/product/product_list.html'
    context_object_name = 'products'


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'shop/product/product_create.html'
    success_url = reverse_lazy('shop:product_list')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    

class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'shop/product/product_update.html'
    success_url = reverse_lazy('shop:product_list')

class ProductDetailView(DetailView):
    model = Product
    template_name = 'shop/product/product_detail.html'

class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'shop/product/product_delete.html'
    success_url = reverse_lazy('shop:product_list')

# Reviews
class ReviewListView(ListView):
    model = Review
    template_name = 'shop/review/review_list.html'
    context_object_name = 'reviews'

class ReviewCreateView(CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'shop/review/review_create.html'
    success_url = reverse_lazy('shop:review_list')
    
    def form_valid(self, form):
        form.instance.reviewer = self.request.user
        return super().form_valid(form)
    

class ReviewUpdateView(UpdateView):
    model = Review
    form_class = ReviewForm
    template_name = 'shop/review/review_update.html'
    success_url = reverse_lazy('shop:review_list')

class ReviewDetailView(DetailView):
    model = Review
    template_name = 'shop/review/review_detail.html'

class ReviewDeleteView(DeleteView):
    model = Review
    template_name = 'shop/review/review_delete.html'
    success_url = reverse_lazy('shop:review_list')

# Orders
class OrderListView(ListView):
    model = Order
    template_name = 'shop/order/order_list.html'
    context_object_name = 'orders'

class OrderCreateView(CreateView):
    model = Order
    form_class = OrderForm
    template_name = 'shop/order/order_create.html'
    success_url = reverse_lazy('shop:order_list')
    
    def form_valid(self, form):
        form.instance.ordered_by = self.request.user
        return super().form_valid(form)

class OrderUpdateView(UpdateView):
    model = Order
    form_class = OrderForm
    template_name = 'shop/order/order_update.html'
    success_url = reverse_lazy('shop:order_list')

class OrderDetailView(DetailView):
    model = Order
    template_name = 'shop/order/order_detail.html'

class OrderDeleteView(DeleteView):
    model = Order
    template_name = 'shop/order/order_delete.html'
    success_url = reverse_lazy('shop:order_list')

class AddToCartView(LoginRequiredMixin, View):
    def post(self, request, product_id):
        cart = request.session.get('cart', {})
        cart[str(product_id)] = cart.get(str(product_id), 0) + 1
        request.session['cart'] = cart
        return redirect('shop:cart_detail')

class CartDetailView(LoginRequiredMixin, View):
    def get(self, request):
        cart = request.session.get('cart', {})
        items = []
        total = 0
        for pid, qty in cart.items():
            product = get_object_or_404(Product, id=pid)
            subtotal = product.price * qty
            items.append({'product': product, 'quantity': qty, 'subtotal': subtotal})
            total += subtotal
        return render(request, 'cart/detail.html', {'items': items, 'total': total})

class CartUpdateView(View):
    def post(self, request):
        orders = Order.objects.filter(ordered_by=request.user, status='PENDING')

        if not orders.exists():
            return redirect('shop:cart')  
        
        for order in orders:
            items = OrderItem.objects.filter(order=order)

            for item in items:
                quantity = request.POST.get(f'quantity_{item.product.id}')
                if quantity:
                    item.quantity = int(quantity)
                    item.save()

            total = sum(item.subtotal() for item in items)  

            return render(request, 'cart/detail.html', {'items': items, 'total': total})

        return redirect('shop:cart')  

    
class CheckoutView(LoginRequiredMixin, View):
    def post(self, request):
        cart = request.session.get('cart', {})
        if not cart:
            return redirect('shop:cart_detail')  

        order = Order.objects.create(
            ordered_by=request.user,
            status='PENDING'
        )

        for product_id, quantity in cart.items():
            product = Product.objects.get(id=product_id)
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity
            )

        request.session['cart'] = {}
        
        return redirect('shop:order_success', order_id=order.id)

class OrderSuccessView(TemplateView):
    template_name = 'cart/success.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order_id = self.kwargs.get('order_id')

        try:
            order = Order.objects.get(id=order_id, ordered_by=self.request.user)
            context['order'] = order
        except Order.DoesNotExist:
            context['order'] = None

        return context