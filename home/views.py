from django.shortcuts import render
from products.models import Product,Category

def home(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    return render(request, "base.html", {
        "products": products,
        "categories": categories,   # ✅ add this
    })

