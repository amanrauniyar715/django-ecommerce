from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
# from .import views
from .models import Luggage, Cart, CartItem, Order
from django.http import HttpResponseForbidden
from django.contrib.auth.models import User  
from decimal import Decimal
from django.contrib import messages
from .forms import RegisterForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login, logout
from .forms import OrderForm
from django.http import HttpResponse
from django.urls import reverse






def registerView(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully. You can now login.")
            return redirect('base:login')
    else:
        form = RegisterForm()
    return render(request, 'base/register.html', {'form': form})

def loginView(request):
    if request.user.is_authenticated:
        return redirect('base:home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('base:home')
        else:
            messages.error(request, "Invalid credentials.")
    return render(request, 'base/login.html')

def logoutView(request):
    logout(request)
    return redirect('base:login')

@login_required(login_url='base:login')
def home_view(request):
    # Your existing home logic
    return render(request, 'base/home.html')

@method_decorator(login_required(login_url='base:login'), name='dispatch')
class HomeView(View):
    def get(self, request):
        # get list of lagguage from model
        
        lugg= Luggage.objects.filter(category="luggage") 
        new= Luggage.objects.filter(category="new") 
        # new=New.objects.all()   
        context = {
            "luggages":lugg,
            "new": new
            # "New":new
            
        }
        
        return render(request, "home.html",context)


class ContactView(View):
    def get(self, request):
        return render(request, "contact.html")


class ProfileView(View):
    def get(self, request):
        return render(request, "profile.html")

class CartView(View):
    def get(self, request):
        return render(request, "cart.html")

class CheckoutView(View):
    def get(self, request):
        return render(request, "checkout.html")

# class ProductDetailView(View):
#     def get(self, request):
#         return render(request, "productdeatil.html")

class dashboardView(View):
    def get(self, request):
        return render(request, "dashboard.html")

class edit_profileView(View):
    def get(self, request):
        return render(request, "edit_profile.html")

class settingsView(View):
    def get(self, request):
        return render(request, "settings.html")

class ProductDetailView(View):
    def get(self, request, id):
        luggage = get_object_or_404(Luggage, id=id)
        # new= New.objects.get(id=id)
        return render(request, "product-detail.html", {"lugg": luggage})


class NewDetailView(View):
    def get(self, request, id):
        new= Luggage.objects.get(id=id)
        # new= New.objects.get(id=id)
        return render(request, "product-detail.html", {"new": new})



class AddToCartView(View):
    def post(self, request, product_id):
        product = get_object_or_404(Luggage, id=product_id)
        user = request.user  # assumes user is logged in

        # Check if item is already in cart
        cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)

        if not created:
            # If already exists, just increment the quantity
            cart_item.quantity += 1
            cart_item.save()

        return redirect('base:cart')  # change to your cart URL name


class CartView(View):
    def get(self, request):
        cart_items = Cart.objects.filter(user=request.user)
        total_price = sum(item.product.price * item.quantity for item in cart_items)

        return render(request, 'cart.html', {
            'cart_items': cart_items,
            'total_price': total_price
        })


# def cart_view(request):
#     cart_items = CartItem.objects.filter(user=request.user)
#     total = sum(item.product.price * item.quantity for item in cart_items)
#     context = {
#         'cart_items': cart_items,
#         'total': total,
#     }
#     return render(request, 'cart.html',{'cart_items': cart_items, 'total': total})


def cart_deleteView(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
    cart_item.delete()
    return redirect('base:cart')

def placeorderView(request, luggage_id):
    luggage = get_object_or_404(Luggage, id=luggage_id)

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.luggage = luggage
            if request.user.is_authenticated:
                order.user = request.user  # ✅ This links the order to the user
            order.save()
            messages.success(request, "Your order has been placed successfully!")
            return redirect(f"{reverse('base:order_success')}?order_id={order.id}")
    else:
        form = OrderForm()

    return render(request, 'base/place_order.html', {'form': form, 'luggage': luggage, 'selected_luggage': luggage})

class OrderSuccessView(View):
    def get(self, request):
        order_id = request.GET.get('order_id')
        print("Received order_id:", order_id)
        return render(request, 'base/order_success.html', {'order_id': order_id})



class SubmitOrderView(View):
    def post(self, request):
        # Get POST data from the form
        product_id = request.POST.get('product_id')
        quantity = request.POST.get('quantity', 1)
        username = request.POST.get('username')
        email = request.POST.get('email')
        shipping_address = request.POST.get('shipping_address')

        # Basic validation
        if not all([product_id, username, email, shipping_address]):
            messages.error(request, "All fields are required.")
            return redirect('base:checkout')

        luggage = get_object_or_404(Luggage, id=product_id)

        # Save to database and store order
        order = Order.objects.create(
            product_id=product_id,
            quantity=quantity,
            username=username,
            email=email,
            shipping_address=shipping_address,
            status="pending"
        )

        success_url = reverse('base:order_success')  # if your URL name is 'order_success'
        return redirect(f"{success_url}?order_id={order.id}")


class CheckoutView(View):
    def get(self, request, luggage_id=None):
        if luggage_id is None:
            return HttpResponse("No luggage selected for checkout.")
        luggage = get_object_or_404(Luggage, id=luggage_id)
        return render(request, 'base/checkout.html', {'lugg': luggage})

    def post(self, request, luggage_id=None):
        # Logic to create/save order goes here
        # For example:
        # Order.objects.create(user=request.user, luggage_id=luggage_id, ...)
        
        # Redirect to success page
        return redirect('base:order_success')


def track_order(request):
    order = None
    error = None

    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        email = request.POST.get('email')

        try:
            order = Order.objects.get(id=order_id, email=email)
        except Order.DoesNotExist:
            error = "No order found with the provided ID and email."

    return render(request, 'base/track_order.html', {'order': order, 'error': error})


@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-id')
    return render(request, 'base/order_history.html', {'orders': orders})

