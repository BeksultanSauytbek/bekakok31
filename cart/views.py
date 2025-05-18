from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from shop.models import Product
from .cart import Cart
from .forms import CartAddProductForm
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product, quantity=cd['quantity'], update_quantity=cd['update'])
    return redirect('cart_detail')


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart_detail')


def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(
            initial={'quantity': item['quantity'], 'update': True})
    return render(request, 'cart/detail.html', {'cart': cart})


@login_required
def send_cart(request):
    cart = Cart(request)
    message = "Новый заказ:\n\n"
    for item in cart:
        message += f"{item['product'].name} - {item['quantity']} x {item['price']}\n"
    message += f"\nИтого: {cart.get_total_price()}"

    send_mail(
        'Новый заказ',
        message,
        settings.EMAIL_HOST_USER,
        ['manager@example.com'],
        fail_silently=False,
    )

    cart.clear()
    return render(request, 'cart/sent.html')