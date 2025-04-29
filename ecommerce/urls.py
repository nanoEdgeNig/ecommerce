from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path, include
from shop.views import IndexView, AboutView, ContactView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('', IndexView.as_view(), name='index'),
    path('about', AboutView.as_view(), name='about'),
    path('contact', ContactView.as_view(), name='contact'),
    path('shop/', include('shop.urls')),
    
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
