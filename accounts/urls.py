from django.urls import path

from . import views
from django.contrib.auth import views as auth_views
from . import views as  accounts_view 
from . import views as  product_view 
from .views import(add_to_cart)
from .models import Carts

urlpatterns = [
    path('',views.home, name='home'),
    path('register',views.register,name='register'),
    path('login',views.login,name='login'),
    path('logout',views.logout,name='logout'),
     path('profile/',accounts_view.profile,name='profile'),
      path('healthcare/',views.healthcare,name='healthcare'),
     path('productspage/', views.get_all_items1, name='productspage'),
      path('ayush/', views.get_all_aitems, name="ayush"),
      path('homeo/', views.get_all_hitems, name="homeo"),
      path('checkout/<str:total>/', views.checkout, name="checkout"),
      path("handlerequest/", views.handlerequest, name="HandleRequest"),
      path("success/",views.success,name="success"),
      path('aproductview/<int:product_id>', product_view.aproductview, name="aproducts"),
      path('hproductview/<int:product_id>', product_view.hproductview, name="hoproducts"),
      path('addTocart/<int:product_id>',views.addTocart,name="addTocart"),
      path('addtocart/<int:product_id>',views.addtocart,name="addtocart"),
      path('promocode/<str:total>/',views.promocode,name="promocode"),
    #   path('<int:product_id>/addcomment/', views.addcomment, name="addcomment"),
    path('productview/<int:product_id>', product_view.productview, name="hproducts"),
    path('cart/',views.cart,name="cart"),
    path('add-to-cart/<int:product_id>',add_to_cart,name="add_to_cart"),
    path('increment/<int:product_id>/',views.increment,name="increment"),
    path('decrement/<int:product_id>/',views.decrement,name="decrement"),
    
    path('search/', views.search,name="search"),
    path('view_order/', views.view_order,name="view_order"),
    path('asearch/', views.asearch,name="search"),
    # path('order-summary/', OrderSummaryView.as_view(), name='order-summary'),
    # path('product/<slug>/', ItemDetailView.as_view(), name='product'),
    # path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
    # path('add-coupon/', AddCouponView.as_view(), name='add-coupon'),
    # path('remove-from-cart/<slug>/', remove_from_cart, name='remove-from-cart'),
    # path('remove-item-from-cart/<slug>/', remove_single_item_from_cart,
    #      name='remove-single-item-from-cart'),
    # path('cart/', views.cart, name="cart"),
    # path('', item_view.get_all_item, name="ecommpath"),

    path('password_reset/',
         auth_views.PasswordResetView.as_view(
             template_name='password_reset.html'
         ),
         name='password_reset'),
    path('password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='password_reset_done.html'
         ),
         name='password_reset_done'),
    path('/password_reset_confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
         ),
         name='password_reset_confirm'),
    path('password_reset_complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='password_reset_complete.html'
         ),
         name='password_reset_complete'),
]
