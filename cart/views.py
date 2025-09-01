from django.shortcuts import render

def cart_list(request):
    return render(request, 'carts/cart_list.html')
