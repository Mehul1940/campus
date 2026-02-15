from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.db import transaction
from datetime import timedelta
import json
from .models import CanteenMenu, FoodOrder, OrderItem, Cart, CartItem
from notifications.models import Notification

# Create your views here.

def menu(request):
    category = request.GET.get('category')
    
    if category:
        menu_items = CanteenMenu.objects.filter(
            available=True,
            category=category
        ).order_by('name')
    else:
        menu_items = CanteenMenu.objects.filter(available=True).order_by('category', 'name')
    
    categories = (
        CanteenMenu.objects
        .filter(available=True)
        .values_list('category', flat=True)
        .distinct()
        .order_by('category')
    )
    
    context = {
        'menu_items': menu_items,
        'categories': categories,
        'selected_category': category,
    }
    return render(request, 'canteen/menu.html', context)

@login_required
def cart_view(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.select_related('menu_item').all()

    total_price = 0
    items_for_template = []
    for item in cart_items:
        item_total = item.menu_item.price * item.quantity
        total_price += item_total
        items_for_template.append({
            'item': item.menu_item,
            'quantity': item.quantity,
            'total': item_total
        })

    context = {
        'cart_items': items_for_template,
        'total_price': total_price,
        'cart_empty': not cart_items.exists(),
    }
    return render(request, 'canteen/cart.html', context)

@require_POST
def add_to_cart(request):
    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'message': 'Please log in first'}, status=401)

    data = json.loads(request.body)
    item_id = data.get('item_id')
    quantity = int(data.get('quantity', 1))

    try:
        menu_item = CanteenMenu.objects.get(id=item_id, available=True)
    except CanteenMenu.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Item not found'}, status=404)

    cart, _ = Cart.objects.get_or_create(user=request.user)

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        menu_item=menu_item,
        defaults={'quantity': quantity}
    )
    if not created:
        cart_item.quantity += quantity
        cart_item.save()

    return JsonResponse({
        'success': True,
        'message': f'{menu_item.name} added to cart!',
        'cart_count': cart.items.count() 
    })

def update_cart(request):
    data = json.loads(request.body)
    item_id = data.get("item_id")
    action = data.get("action")

    try:
        cart = Cart.objects.get(user=request.user)
        cart_item = CartItem.objects.get(cart=cart, menu_item_id=item_id)

        if action == "increase":
            cart_item.quantity += 1
            cart_item.save()
        elif action == "decrease":
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
            else:
                cart_item.delete()
        elif action == "remove":
            cart_item.delete()
        else:
            return JsonResponse({"success": False, "message": "Invalid action"})

        return JsonResponse({"success": True})

    except Cart.DoesNotExist:
        return JsonResponse({"success": False, "message": "Cart not found"})
    except CartItem.DoesNotExist:
        return JsonResponse({"success": False, "message": "Item not in cart"})

@login_required
@require_POST
def remove_from_cart(request):
    data = json.loads(request.body)
    item_id = data.get('item_id')

    cart = get_object_or_404(Cart, user=request.user)
    CartItem.objects.filter(cart=cart, menu_item_id=item_id).delete()

    return JsonResponse({'success': True})

@login_required
def checkout(request):
    cart = get_object_or_404(Cart, user=request.user)
    cart_items = cart.items.select_related('menu_item').all()

    if not cart_items.exists():
        messages.error(request, "Your cart is empty!")
        return redirect('canteen:menu')

    subtotal = cart.subtotal 

    if request.method == 'POST':
        special_instructions = request.POST.get('special_instructions', '')

        with transaction.atomic():

            order = FoodOrder.objects.create(
                user=request.user,
                special_instructions=special_instructions,
                status='pending',
                total_amount=subtotal,
                pickup_time=timezone.now() + timedelta(minutes=30)
            )

            for cart_item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    menu_item=cart_item.menu_item,
                    quantity=cart_item.quantity,
                    item_price=cart_item.menu_item.price
                )

            cart_items.delete()

            Notification.objects.create(
                user=request.user,
                title='Order Confirmed',
                message=f'Your order #{order.id} has been placed. Pickup at {order.pickup_time.strftime("%H:%M")}',
                notification_type='order',
                related_order=order
            )

        messages.success(
            request,
            f'Order placed! Pickup at {order.pickup_time.strftime("%H:%M")}'
        )

        return redirect('canteen:order_detail', order_id=order.id)

    context = {
        'cart_items': cart_items,
        'subtotal': subtotal,
    }

    return render(request, 'canteen/checkout.html', context)

@login_required
def order_history(request):
    orders = FoodOrder.objects.filter(user=request.user).prefetch_related('items')
    
    context = {
        'orders': orders,
    }
    return render(request, 'canteen/order_history.html', context)


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(FoodOrder, id=order_id, user=request.user)
    order_items = OrderItem.objects.filter(order=order)
    for item in order_items:
        item.total_price = item.item_price * item.quantity
    
    context = {
        'order': order,
        'order_items': order_items,
    }
    return render(request, 'canteen/order_detail.html', context)

@login_required
def cancel_order(request, order_id):
    order = get_object_or_404(FoodOrder, id=order_id, user=request.user)
    if order.cancel_order():
        messages.success(request, f"Order #{order.id} has been cancelled successfully.")
    else:
        messages.error(request, f"Order #{order.id} cannot be cancelled at this stage.")
    return redirect('canteen:order_history')