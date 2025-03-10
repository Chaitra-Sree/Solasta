import json
from django.db import models
from datetime import datetime
import uuid  # Import UUID for unique tracking IDs
from django.contrib.auth.models import User



# Create your models here.

class Category(models.Model):
    category_title = models.CharField(max_length=100)
    category_description = models.TextField()
    category_gif = models.CharField(max_length=200)  # Assuming this is the image URL
    button_label = models.CharField(max_length=100, default="Order")
    
    

    def __str__(self):
        return self.category_title

class RegularPizza(models.Model):
    #example row :: 1 topping , 5.00 , 7.00
    pizza_choice = models.CharField(max_length=200)
    small_price = models.DecimalField(max_digits=6, decimal_places=2)
    large_price = models.DecimalField(max_digits=6, decimal_places=2)
    category_description = models.TextField() #make this the wysiwyg text field

    def __str__(self):
        #overriding the string method to get a good representation of it in string format
        return f"Regular Pizza : {self.pizza_choice}"

class SicilianPizza(models.Model):
    #example row :: 1 topping , 5.00 , 7.00
    pizza_choice = models.CharField(max_length=200)
    small_price = models.DecimalField(max_digits=6, decimal_places=2)
    large_price = models.DecimalField(max_digits=6, decimal_places=2)
    category_description = models.TextField() #make this the wysiwyg text field

    def __str__(self):
        #overriding the string method to get a good representation of it in string format
        return f"Sicilian Pizza : {self.pizza_choice}"

class Toppings(models.Model):
    #example row :: Pepperoni
    topping_name = models.CharField(max_length=200)

    def __str__(self):
        #overriding the string method to get a good representation of it in string format
        return f"{self.topping_name}"


class Sub(models.Model):
    #example row :: meatball , 5.00 , 6.50
    sub_filling = models.CharField(max_length=200)
    small_price = models.DecimalField(max_digits=6, decimal_places=2)
    large_price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        #overriding the string method to get a good representation of it in string format
        return f"Sub : {self.sub_filling}"

class Pasta(models.Model):
    dish_name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        #overriding the string method to get a good representation of it in string format
        return f"{self.dish_name}"


class Salad(models.Model):
    dish_name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        #overriding the string method to get a good representation of it in string format
        return f"Salad : {self.dish_name}"



class DinnerPlatters(models.Model):
    dish_name = models.CharField(max_length=200)
    small_price = models.DecimalField(max_digits=6, decimal_places=2)
    large_price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        #overriding the string method to get a good representation of it in string format
        return f"Platter : {self.dish_name}"

class UserOrder(models.Model):
    username = models.CharField(max_length=200) #who placed the order
    order = models.TextField() #this will be a string representation of the cart from localStorage
    price = models.DecimalField(max_digits=6, decimal_places=2) #how much was the order
    time_of_order  = models.DateTimeField(default=datetime.now, blank=True)
    delivered = models.BooleanField()

    def __str__(self):
        #overriding the string method to get a good representation of it in string format
        return f"Order placed by  : {self.username} on {self.time_of_order.date()} at {self.time_of_order.time().strftime('%H:%M:%S')}"

class SavedCarts(models.Model):
    username = models.CharField(max_length=200, primary_key=True)
    cart = models.TextField() #this will be a string representation of the cart from localStorage

    def __str__(self):
        #overriding the string method to get a good representation of it in string format
        return f"Saved cart for {self.username}"
    

class CartItem(models.Model):
    product = models.CharField(max_length=255)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product} - ${self.price}"

class Order(models.Model):
    tracking_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)  # Auto-generate Tracking ID
    items = models.ManyToManyField(CartItem, blank=True)  # Order has multiple items
    placed = models.BooleanField(default=False)  # Status field

    def __str__(self):
        return f"Order {self.tracking_id} - {'Placed' if self.placed else 'Pending'}"
    

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def checkout(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            cart = data.get('cart', [])
            price = data.get('price_of_cart', 0)
            username = request.user.username

            order = UserOrder(username=username, order=str(cart), price=float(price), delivered=False)
            order.save()

            return JsonResponse({'result': 'Order Received!'}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    return JsonResponse({"error": "Invalid request"}, status=400)

