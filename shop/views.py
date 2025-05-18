from django.shortcuts import render, get_object_or_404
from .models import Category, Product, Brand
from cart.forms import CartAddProductForm


def home(request):
    categories = Category.objects.filter(parent=None)
    brands = Brand.objects.all()
    return render(request, 'home.html', {'categories': categories, 'brands': brands})


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    return render(request, 'products.html', {
        'category': category,
        'categories': categories,
        'products': products,
    })


def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    cart_product_form = CartAddProductForm()
    return render(request, 'product_detail.html', {
        'product': product,
        'cart_product_form': cart_product_form,
    })


def about(request):
    return render(request, 'about_us.html')


def contact(request):
    if request.method == 'POST':
        # Обработка формы контактов
        pass
    return render(request, 'contact.html')