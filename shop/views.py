from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import (
    TemplateView, CreateView, ListView, 
    DetailView, UpdateView, DeleteView, View
)
from .models import Category, Product, Order, OrderItem, Review
from .forms import CategoryForm, ProductForm, ReviewForm, OrderForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.db.models import F
from django.contrib import messages

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
        product = get_object_or_404(Product, id=product_id)
        try:
            qty = max(int(request.POST.get('quantity', 1)), 1)
        except ValueError:
            qty = 1
        order = (
            Order.objects
                 .filter(ordered_by=request.user, status='PENDING')
                 .order_by('-ordered_on')
                 .first()
        )
        if not order:
            order = Order.objects.create(
                ordered_by=request.user,
                status='PENDING',
                ordered_on=timezone.now()
            )
        item, created = OrderItem.objects.get_or_create(
            order=order,
            product=product,
            defaults={'quantity': 0}
        )
        item.quantity += qty
        item.save()
        return redirect('shop:cart_detail')

class CartDetailView(LoginRequiredMixin, View):
    def get(self, request):
        order = Order.objects.filter(
            ordered_by=request.user, status='PENDING'
        ).order_by('-ordered_on').first()
        items = order.items.select_related('product') if order else []
        total = sum(item.subtotal() for item in items)
        return render(request, 'cart/detail.html', {
            'items': items,
            'total': total
        })

class CartUpdateView(LoginRequiredMixin, View):
    def post(self, request):
        order = Order.objects.filter(
            ordered_by=request.user, status='PENDING'
        ).order_by('-ordered_on').first()
        if not order:
            messages.error(request, "You have no items in your cart.")
            return redirect('shop:cart_detail')
        updated = False
        for key, raw in request.POST.items():
            if not key.startswith('quantity_'):
                continue
            try:
                pid = int(key.split('_', 1)[1])
                new_q = int(raw)
            except (ValueError, IndexError):
                continue
            try:
                item = OrderItem.objects.get(order=order, product_id=pid)
            except OrderItem.DoesNotExist:
                continue
            if new_q <= 0:
                item.delete()
                updated = True
            elif new_q != item.quantity:
                item.quantity = new_q
                item.save()
                updated = True
        if not order.items.exists():
            order.delete()
        if updated:
            messages.success(request, "Your cart has been updated.")
        else:
            messages.info(request, "No changes detected in your cart.")
        return redirect('shop:cart_detail')

class CheckoutView(LoginRequiredMixin, View):
    def post(self, request):
        order = Order.objects.filter(
            ordered_by=request.user, status='PENDING'
        ).order_by('-ordered_on').first()
        if not order or not order.items.exists():
            messages.error(request, "Your cart is empty.")
            return redirect('shop:cart_detail')
        for item in order.items.select_related('product'):
            if item.product.stock < item.quantity:
                messages.error(
                    request,
                    f"Not enough stock for {item.product.product_name} "
                    f"(only {item.product.stock} left)."
                )
                return redirect('shop:cart_detail')
        for item in order.items.all():
            Product.objects.filter(id=item.product.id) \
                           .update(stock=F('stock') - item.quantity)
        order.status = 'PLACED'
        order.ordered_on = timezone.now()
        order.save()
        messages.success(request, "Order placed successfully!")
        return redirect('shop:order_success', order_id=order.id)

class OrderSuccessView(TemplateView):
    template_name = 'cart/success.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order_id = self.kwargs.get('order_id')
        context['order'] = Order.objects.filter(
            id=order_id,
            ordered_by=self.request.user
        ).first()
        return context
