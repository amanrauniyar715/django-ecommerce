# from django.urls import path
# from .views import HomeView, ContactView, ProfileView, CartView, CheckoutView, ProductDetailView, dashboardView, edit_profileView, settingsView


# app_name = "base"
# urlpatterns = [
#     path("", HomeView.as_view(), name="home"),
#     path("contact/", ContactView.as_view(), name="contact"),
#     path("profile/", ProfileView.as_view(), name="profile"),
#     path("cart/", CartView.as_view(), name="cart"),
#     path("checkout/", CheckoutView.as_view(), name="checkout"),
#     path('dashboard/', dashboardView.as_view(), name='user_dashboard'),
#     path('profile/edit/', edit_profileView.as_view(), name='edit_profile'),
#     # path('orders/', views.order_history, name='order_history'),
#     # path('orders/<int:order_id>/', views.order_detail, name='order_detail'),
#     path('settings/', settingsView.as_view(), name='user_settings'),
#     # path('settings/change-password/', views.change_password, name='change_password'),
#     # path('shipping-addresses/', views.shipping_addresses, name='shipping_addresses'),
#     # path('shipping-addresses/add/', views.add_shipping_address, name='add_shipping_address'),
#     # path('shipping-addresses/<int:address_id>/edit/', views.edit_shipping_address, name='edit_shipping_address'),
#     # path('shipping-addresses/<int:address_id>/delete/', views.delete_shipping_address, name='delete_shipping_address'),
#     path('product/<int:id>/', ProductDetail.as_view(), name='product-detail'),
# ]



from django.urls import path
from django.contrib.auth.views import LogoutView 
from .views import (
    HomeView, ContactView, ProfileView, CheckoutView,
    ProductDetailView, dashboardView, edit_profileView, settingsView, NewDetailView, AddToCartView, CartView, cart_deleteView, SubmitOrderView,
    loginView, registerView, logoutView, OrderSuccessView, placeorderView, CheckoutView,  track_order,
    order_history
)

app_name = "base"

urlpatterns = [
    path("", loginView, name="login"),
    path("home/", HomeView.as_view(), name="home"),
    path('register/',registerView, name='register'),
    path('login/', loginView, name='login'),
    path('logout/', logoutView, name='logout'),
    path("contact/", ContactView.as_view(), name="contact"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("cart/", CartView.as_view(), name="cart"),
    
    path("checkout/", CheckoutView.as_view(), name="checkout"),
    path("checkout/<int:luggage_id>/", CheckoutView.as_view(), name='checkout'),
    path('dashboard/', dashboardView.as_view(), name='user_dashboard'),
    path('profile/edit/', edit_profileView.as_view(), name='edit_profile'),
    path('settings/', settingsView.as_view(), name='user_settings'),
    path('place-order/<int:luggage_id>/', placeorderView, name='place_order'),
    # ✅ Correct product detail route
    path('product/<int:id>/', ProductDetailView.as_view(), name='product-detail'),
    # In base/urls.py

    path('add-to-cart/<int:product_id>/', AddToCartView.as_view(), name='add-to-cart'),
    path('cart/', CartView.as_view(), name='cart'),
    path('cart/delete/<int:item_id>/', cart_deleteView, name='cart_delete'),
   
    path('submit-order/', SubmitOrderView.as_view(), name='submit_order'),
   
    path('order-success/', OrderSuccessView.as_view(), name='order_success'),
    path('logout/', LogoutView.as_view(next_page='base:login'), name='logout'),
    # urls.py
    # path('track-order/<int:luggage_id>', trackorderView, name='track_order'),
    path('track-order/', track_order, name='track_order'),
    path('my-orders/', order_history, name='order_history'),
    
]
