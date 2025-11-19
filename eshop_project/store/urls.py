from django.urls import path
from . import views
   
urlpatterns = [
    # 🏠 Home & Core Pages
    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),

    # 👤 Authentication
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # 🛍️ Product Pages
    path('products/', views.product_list, name='product_list'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),

    # 🧩 Category Pages
    path('categories/', views.categories, name='categories'),
    path('handcraft/', views.handcraft_page, name='handcraft'),
    path('gift/', views.gift_page, name='gift'),
    path('clothing/', views.clothing_page, name='clothing'),

    # 🛒 Cart & Orders
    path('cart/', views.cart_view, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('create_order/', views.create_order, name='create_order'),
    path('order/', views.order_form, name='order_form'),

    # 💳 Payment
    path('payment/<int:product_id>/', views.payment_page, name='payment'),
    path('process_payment/', views.process_payment, name='process_payment'),

    # 💳 Payment initiation
    path('payment/<int:product_id>/', views.payment_page, name='payment'),

    # 🧾 Razorpay verification endpoint (used in JS fetch)
    path('verify-payment/', views.verify_payment, name='verify_payment'),

    # 💸 Placeholder or post-payment logic
    path('process_payment/', views.process_payment, name='process_payment'),
]



