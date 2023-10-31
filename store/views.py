from django.shortcuts import render, get_object_or_404
from .models import Product
from carts.models import CartItem
from category.models import Category
from carts.views import _cart_id
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse
from django.db.models import Q

from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from .models import Product, Category

def home(request):
    products = Product.objects.all().filter(is_available=True)

    context = {
        'products': products,
    }

    return render(request, 'home.html', context)

def store(request, category_slug=None, product_slug=None):
    categories = Category.objects.all()
    products = None
    product_count = 0

    if category_slug is not None:
        category = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=category, is_available=True)
        paginator = Paginator(products, 3)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()
    else:
        products = Product.objects.filter(is_available=True).order_by('id')
        paginator = Paginator(products, 3)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()

    context = {
        'categories': categories,
        'products': products,
        'product_count': product_count,
    }

    return render(request, 'store/store.html', context)
    context = {
        'products': paged_products,
        'product_count': product_count,
        'categories': categories,
    }
    return render(request, 'store/store.html', context)

def product_detail(request, category_slug, product_slug):
    product = get_object_or_404(Product, slug=product_slug, category__slug=category_slug, is_available=True)
    context = {
        'product': product,
    }
    try:
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists()
    except Exception as e:
        raise e
        
    context = {
    'single_product': single_product,
    'in_cart'       : in_cart,
    }   
    return render(request, 'store/product_detail.html', context) 
    
def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('-created_date').filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword))
    context = {
        'products': products,
    }
    return render(request, 'store/store.html', context)
