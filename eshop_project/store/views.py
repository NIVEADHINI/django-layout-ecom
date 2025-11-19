from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.urls import reverse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import razorpay

from .models import Product, Category, Order
from .forms import OrderCreateForm

# 🔐 Login
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        next_page = request.POST.get('next') or reverse('home')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(next_page)
        else:
            messages.error(request, "Invalid credentials.")
            return render(request, 'store/login.html', {
                'next': next_page
            })

    return render(request, 'store/login.html', {
        'next': request.GET.get('next', '')
    })

# 👤 Signup
def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('signup')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('signup')

        user = User.objects.create_user(username=username, email=email, password=password)
        messages.success(request, "Account created! Please log in.")
        return redirect('login')
    return render(request, 'store/signup.html')

# 🚪 Logout
def logout_view(request):
    logout(request)
    messages.info(request, "Logged out successfully.")
    return redirect('login')

# 🏠 Home
def home(request):
    products = Product.objects.all()
    return render(request, 'store/home.html', {'products': products})

# 👕 Clothing
def clothing_page(request):
    products = Product.objects.filter(category__name__icontains="clothing")
    return render(request, 'store/clothing.html', {'products': products})

# 💍 Handcraft
def handcraft_page(request):
    products = Product.objects.filter(category__name__icontains="handcraft")
    return render(request, 'store/handcraft.html', {'products': products})

# 🎁 Gift
def gift_page(request):
    products = Product.objects.filter(category__name__icontains="gift")
    return render(request, 'store/gift.html', {'products': products})

# 💳 Payment with Razorpay
@login_required
def payment_page(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    amount = int(product.price * 100)

    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
    order = client.order.create({
        "amount": amount,
        "currency": "INR",
        "payment_capture": "1"
    })

    context = {
        "product": product,
        "amount": amount,
        "order_id": order['id'],
        "razorpay_key": settings.RAZORPAY_KEY_ID,
        "user": request.user
    }
    return render(request, 'store/payment.html', context)

# ✅ Razorpay Signature Verification
@csrf_exempt
def verify_payment(request):
    if request.method == "POST":
        data = request.POST
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

        try:
            client.utility.verify_payment_signature({
                'razorpay_order_id': data['razorpay_order_id'],
                'razorpay_payment_id': data['razorpay_payment_id'],
                'razorpay_signature': data['razorpay_signature']
            })
            # ✅ Save payment info to database here
            return HttpResponse("Payment verified successfully.")
        except razorpay.errors.SignatureVerificationError:
            return HttpResponse("Payment verification failed.")

# 💸 Process Payment (placeholder)
def process_payment(request):
    return HttpResponse("Payment processing placeholder.")

# 📦 Product Detail
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'store/product_detail.html', {'product': product})

# 🧾 Create Order
def create_order(request):
    if request.method == "POST":
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            messages.success(request, "Order created successfully!")
            return redirect('payment', product_id=order.product.id)
    else:
        form = OrderCreateForm()
    return render(request, 'store/order_form.html', {'form': form})

# 🛒 Cart
def cart_view(request):
    return render(request, 'store/cart.html')

# 💬 Contact
def contact(request):
    return render(request, 'store/contact.html')

# 📋 Product List
def product_list(request):
    return HttpResponse("Product list working!")

# 📚 Categories
def categories(request):
    return HttpResponse("Categories page coming soon.")

# 💰 Checkout
def checkout(request):
    return render(request, 'store/checkout.html')

# 🧾 Order Form (placeholder)
def order_form(request):
    return HttpResponse("Order form placeholder.")