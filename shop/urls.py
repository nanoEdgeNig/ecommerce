from django.urls import path
from .views import (
    CategoryListView, CategoryCreateView, CategoryUpdateView, CategoryDetailView, CategoryDeleteView,
    ProductListView, ProductCreateView, ProductUpdateView, ProductDetailView, ProductDeleteView,
    ReviewListView, ReviewCreateView, ReviewUpdateView, ReviewDetailView, ReviewDeleteView,
    OrderListView, OrderCreateView, OrderUpdateView, OrderDetailView, OrderDeleteView,
    DashboardIndexView, AddToCartView, CartDetailView, CheckoutView, CartUpdateView, OrderSuccessView
    
)

app_name = 'shop'

urlpatterns = [
    
    path('dashboard/', DashboardIndexView.as_view(), name='dashboard'),
    #categories
    path('categories/', CategoryListView.as_view(), name='category_list'),
    path('categories/create/', CategoryCreateView.as_view(), name='category_create'),
    path('categories/<int:pk>/update/', CategoryUpdateView.as_view(), name='category_update'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category_detail'),
    path('categories/<int:pk>/delete/', CategoryDeleteView.as_view(), name='category_delete'),
    
    # product
    path('products/', ProductListView.as_view(), name='product_list'),
    path('products/create/', ProductCreateView.as_view(), name='product_create'),
    path('products/<int:pk>/update/', ProductUpdateView.as_view(), name='product_update'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('products/<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),
    
    # review
    path('reviews/', ReviewListView.as_view(), name='review_list'),
    path('reviews/create/', ReviewCreateView.as_view(), name='review_create'),
    path('reviews/<int:pk>/update/', ReviewUpdateView.as_view(), name='review_update'),
    path('reviews/<int:pk>/', ReviewDetailView.as_view(), name='review_detail'),
    path('reviews/<int:pk>/delete/', ReviewDeleteView.as_view(), name='review_delete'),
    
    # order
    path('orders/', OrderListView.as_view(), name='order_list'),
    path('orders/create/', OrderCreateView.as_view(), name='order_create'),
    path('orders/<int:pk>/update/', OrderUpdateView.as_view(), name='order_update'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order_detail'),
    path('orders/<int:pk>/delete/', OrderDeleteView.as_view(), name='order_delete'),
    
    # carts
    path('cart/add/<int:product_id>/', AddToCartView.as_view(), name='add_to_cart'),
    path('cart/', CartDetailView.as_view(), name='cart_detail'),
    path('cart/update/', CartUpdateView.as_view(), name='cart_update'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('cart/success/<int:order_id>/', OrderSuccessView.as_view(), name='order_success'),
]
