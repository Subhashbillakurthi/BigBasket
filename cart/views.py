import json
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import CartItem
from products.models import Product,Category

@login_required
@require_POST
def add_to_cart(request, product_id):
    try:
        data = json.loads(request.body)
        quantity = int(data.get('quantity', 1))
    except (ValueError, json.JSONDecodeError):
        return HttpResponseBadRequest("Invalid data")
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.quantity += quantity
    else:
        cart_item.quantity = quantity
    cart_item.save()
    return JsonResponse({'status': 'success', 'quantity': cart_item.quantity})

@login_required
def cart_view(request):
    items = CartItem.objects.filter(user=request.user).select_related('product')
    categories = Category.objects.all()
    subtotal = sum(item.total_price for item in items)
    total_items = sum(item.quantity for item in items)
    savings = sum(item.saved for item in items)
    return render(request, 'cart/cart.html', {
        'cart_items': items,
        'subtotal': subtotal,
        'total_items': total_items,
        'savings': savings,
        'categories':categories,
    })

@login_required
@require_POST
def update_cart_quantity(request, item_id):
    try:
        data = json.loads(request.body)
        qty = int(data.get('quantity', 1))
    except (ValueError, json.JSONDecodeError):
        return HttpResponseBadRequest("Invalid data")
    cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
    cart_item.quantity = max(1, qty)
    cart_item.save()
    return JsonResponse({
        'status': 'success',
        'quantity': cart_item.quantity,
        'row_total': float(cart_item.total_price),
        'subtotal': float(sum(i.total_price for i in CartItem.objects.filter(user=request.user))),
        'savings': float(sum(i.saved for i in CartItem.objects.filter(user=request.user))),
        'total_items': sum(i.quantity for i in CartItem.objects.filter(user=request.user)),
    })

@login_required
@require_POST
def delete_cart_item(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
    cart_item.delete()
    return JsonResponse({'status': 'success'})
