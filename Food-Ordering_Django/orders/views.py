from django.http import HttpResponse
from django.shortcuts import render,redirect
from .models import Category, RegularPizza, SicilianPizza, Toppings, Sub, Pasta, Salad, DinnerPlatters, UserOrder, SavedCarts
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import logout, authenticate, login
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.conf import settings
import paypalrestsdk
import datetime
from django.urls import reverse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
import logging
from django.http import HttpResponse
from django.shortcuts import redirect
import paypalrestsdk
from django.conf import settings




def index(request):
    # If the user is authenticated, render the home page
    if request.user.is_authenticated:
        print("User is authenticated")
        return render(request, "orders/home.html", {"categories": Category.objects.all()})
    
    # Allow guest access if 'qr_access' parameter is provided in the URL
    elif request.GET.get('qr_access') == '1':
        print("QR access granted")
        return render(request, "orders/home.html", {"categories": Category.objects.all()})
    
    # For all other cases, redirect to login
    else:
        print("Redirecting to login")
        return redirect("orders:login")






def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')  
        else:
           
            return render(request, 'orders/login.html', {'form': form})

    
    form = AuthenticationForm()
    return render(request, 'orders/login.html', {'form': form})

logger = logging.getLogger(__name__)
def logout_request(request):
    logger.info("Logout request triggered for user: %s", request.user)
    logout(request)
    logger.info("User successfully logged out.")
    return redirect("orders:login")

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            login(request, user)
            return redirect("orders:index")

        return render(request,
                      template_name="orders/register.html",
                      context={"form": form})

    return render(request,
                  template_name="orders/register.html",
                  context={"form": UserCreationForm()})

def pizza(request):
    print("qr_access in session:", request.session.get('qr_access'))
    if request.user.is_authenticated or request.session.get('qr_access') == '1':
        return render(request, "orders/pizza.html", context={
            "regular_pizza": RegularPizza.objects.all(),
            "sicillian_pizza": SicilianPizza.objects.all(),
            "toppings": Toppings.objects.all(),
            "number_of_toppings": [1, 2, 3]
        })
    else:
        return redirect("orders:login")



def pasta(request):
    if request.user.is_authenticated or request.session.get('qr_access') == '1':
        return render(request, "orders/pasta.html", context={"dishes": Pasta.objects.all()})
    else:
        return redirect("orders:login")



def salad(request):
    if request.user.is_authenticated or request.session.get('qr_access') == '1':
        return render(request, "orders/salad.html", context={"dishes": Salad.objects.all()})
    else:
        return redirect("orders:login")



def tacos(request):
    if request.user.is_authenticated or request.session.get('qr_access') == '1':
        return render(request, "orders/tacos.html", context = {"dishes":Sub.objects.all})
    else:
        return redirect("orders:login")


def platters(request):
    if request.user.is_authenticated or request.session.get('qr_access') == '1':
        # Use parentheses to call the method and get the query results
        dishes = DinnerPlatters.objects.all()
        print(dishes)  # Add a debug print statement to check the data
        return render(request, "orders/platters.html", context={"dishes": dishes})
    else:
        return redirect("orders:login")


# Static Pages
def directions(request):
    if request.user.is_authenticated or request.session.get('qr_access') == '1':
        return render(request, "orders/directions.html")
    else:
        return redirect("orders:login")

def aboutus(request):
    if request.user.is_authenticated or request.session.get('qr_access') == '1':
        return render(request, "orders/aboutus.html")
    else:
        return redirect("orders:login")

def contact(request):
    if request.user.is_authenticated or request.session.get('qr_access') == '1':
        return render(request, "orders/contact.html")
    else:
        return redirect("orders:login")

def cart(request):
    if request.user.is_authenticated or request.session.get('qr_access') == '1':
        return render(request, "orders/cart.html")
    else:
        return redirect("orders:login")

def checkout(request):
    if request.method == 'POST':
        cart = json.loads(request.POST.get('cart'))
        price = request.POST.get('price_of_cart')
        username = request.user.username
        response_data = {}
        list_of_items = [item["item_description"] for item in cart]

        order = UserOrder(username=username, order=list_of_items, price=float(price), delivered=False) 
        order.save() 

        billing_details = {
            'name': request.POST.get('name', 'Not Provided'),
            'email': request.POST.get('email', 'Not Provided'),
            'address': request.POST.get('address', 'Not Provided'),
            'city': request.POST.get('city', 'Not Provided'),
            'state': request.POST.get('state', 'Not Provided'),
            'zip': request.POST.get('zip', 'Not Provided'),
        }

        request.session['billing_details'] = billing_details

        response_data['result'] = 'Order Recieved!'

        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )

def view_orders(request):
    if request.user.is_superuser:
       
        rows = UserOrder.objects.all().order_by('-time_of_order')
       
        return render(request, "orders/orders.html", context = {"rows":rows})
    else:
        rows = UserOrder.objects.all().filter(username = request.user.username).order_by('-time_of_order')
        return render(request, "orders/orders.html", context = {"rows":rows})

def mark_order_as_delivered(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        UserOrder.objects.filter(pk=id).update(delivered=True)
        return HttpResponse(
            json.dumps({"good":"boy"}),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )

def save_cart(request):
    if request.method == 'POST':
        cart = request.POST.get('cart')
        saved_cart = SavedCarts(username=request.user.username, cart=cart) 
        saved_cart.save() 
        return HttpResponse(
            json.dumps({"good":"boy"}),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )



def retrieve_saved_cart(request):
    try:
        saved_cart = SavedCarts.objects.get(username=request.user.username)
       
        cart_data = saved_cart.cart if saved_cart.cart else '[]' 
        return JsonResponse({'cart': cart_data}, safe=False)
    except SavedCarts.DoesNotExist:
       
        return JsonResponse({'cart': '[]'}, safe=False)


def check_superuser(request):
    print(f"User super??? {request.user.is_superuser}")
    return HttpResponse(request.user.is_superuser)
















def payment_page(request):
    amount = request.POST.get('amount', '0')  # Get the amount from the POST request
    return render(request, 'orders/payment.html', {'amount': amount})  # Pass the amount to the template
   
   

def checkout_button(request):
    return render(request, 'orders/checkout_btn.html')

import paypalrestsdk
from django.conf import settings
from django.shortcuts import render, redirect

paypalrestsdk.configure({                                  
    "mode": settings.PAYPAL_ENVIRONMENT, 
    "client_id": settings.PAYPAL_CLIENT_ID,
    "client_secret": settings.PAYPAL_CLIENT_SECRET
})



def payment_process(request):
    amount = request.POST.get('amount', '0')  

    payment = paypalrestsdk.Payment({   
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"
        },
        "redirect_urls": {
            "return_url": "http://127.0.0.1:8000/payment_success/",
            "cancel_url": "http://127.0.0.1:8000/payment_cancel/"
        },
        "transactions": [{
            "amount": {
                "total": f"{float(amount):.2f}",
                "currency": "USD"
            },
            "description": "Payment for Order"
        }]
    })

    if payment.create(): 
        for link in payment.links:
            if link.rel == "approval_url":
                return redirect(link.href)  
    else:
        return render(request, "orders/payment_failed.html", {"error": payment.error})

def payment_success(request):
    billing_details = {
        'name': request.GET.get('name', 'Not Provided'),
        'email': request.GET.get('email', 'Not Provided'),
        'address': request.GET.get('address', 'Not Provided'),
        'city': request.GET.get('city', 'Not Provided'),
        'state': request.GET.get('state', 'Not Provided'),
        'zip': request.GET.get('zip', 'Not Provided'),
    }
    return render(request, "orders/payment_success.html")



def payment_cancel(request):
    return render(request, "orders/payment_cancel.html")

def retrieve_saved_cart(request):
    
    return JsonResponse({'status': 'success'})







