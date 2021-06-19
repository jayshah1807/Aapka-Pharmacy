
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('accounts.urls')),
    
    path('accounts/',include('allauth.urls')),
    path('products1/', include("accounts.urls"), name="productspage"),
]
urlpatterns = urlpatterns + \
static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
