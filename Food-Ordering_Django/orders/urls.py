from django.urls import path

from . import views



app_name = "orders"

urlpatterns = [
    path("", views.index, name="index"),
    path('qr-code/', views.qr_code_view, name='qr_code'),

    path("login/", views.login_request, name="login"),
    path("register/", views.register, name="register"),
    path("logout/", views.logout_request, name="logout"),
    path("pizza/", views.pizza, name="pizza"),
    path("pasta/", views.pasta, name="pasta"),
    path("salad/", views.salad, name="salad"),
    path("tacos/", views.tacos, name="tacos"),
    path("platters/", views.platters, name="platters"),
    path("directions/", views.directions, name="directions"),
    path("hours/", views.aboutus, name="aboutus"),
    path("contact/", views.contact, name="contact"),
    path("cart/", views.cart, name="cart"),
    path("checkout/", views.checkout, name="checkout"),
    path("view-orders/", views.view_orders, name="view-orders"),
    path("checkout_btn/",views.checkout_button,name="checkout_button"),
    path("mark_order_as_delivered/", views.mark_order_as_delivered, name="mark_order_as_delivered"),
    path("save_cart/", views.save_cart, name="save_cart"),
    path("retrieve_saved_cart/", views.retrieve_saved_cart, name="retrieve_saved_cart"),
    path('payment/', views.payment_page, name='payment_page'),
    path('payment_process/', views.payment_process, name='payment_process'),
    path('payment_success/', views.payment_success, name='payment_success'),
     path('payment_success/retrieve_saved_cart/', views.retrieve_saved_cart, name='retrieve_saved_cart'),
    path('payment_cancel/', views.payment_cancel, name='payment_cancel'),
    path("check_superuser/", views.check_superuser, name="check_superuser"),
     
    
    
    ]
