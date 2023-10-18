from django.shortcuts import render, get_object_or_404
from .models import Product
from category.models import Category
def home(request):
    products = Product.objects.all().filter(is_available=True)

    context = {
        'products': products,
    }

    return render(request, 'home.html', context)



def store(request, category_slug=None, product_slug=None):  # Ajout de product_slug
    categories = Category.objects.all()
    products = None
    product_count = 0

    if category_slug:
        selected_category = get_object_or_404(Category, slug=category_slug)
        if product_slug:  # Si product_slug est fourni, obtenez un produit spécifique
            product = get_object_or_404(Product, slug=product_slug, category=selected_category, is_available=True)
            # Ajoutez ici le code pour gérer la vue d'un produit spécifique (product_detail)
            return render(request, 'store/product_detail.html', {'product': product})
        else:
            # Sinon, obtenez tous les produits de la catégorie sélectionnée
            products = Product.objects.filter(category=selected_category, is_available=True)
        product_count = products.count()
    else:
        # Si aucune catégorie n'est sélectionnée, obtenez tous les produits disponibles
        products = Product.objects.filter(is_available=True)
        product_count = products.count()

    context = {
        'products': products,
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
    except Exception as e:
        raise e
        
    context = {
    'single_product': single_product,
    }   
    return render(request, 'store/product_detail.html', context) 
    

