from django.shortcuts import render, redirect, get_object_or_404
from shop.models import product
from .models import Cart, CartItem, Wishlist
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required


# Create your views here.
def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def add_cart(request, product_id):
    products = product.objects.get(id=product_id)
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except ObjectDoesNotExist:
        cart = Cart.objects.create(
            cart_id=_cart_id(request)
        )
        cart.save(),
    try:
        cart_item = CartItem.objects.get(product=products, cart=cart)
        if cart_item.quantity < cart_item.product.stock:
            cart_item.quantity += 1
            cart_item.save()
    except ObjectDoesNotExist:
        cart_item = CartItem.objects.create(
            product=products,
            quantity=1,
            cart=cart
        )
        cart_item.save()
    return redirect('cart:cart_detail')


def cart_detail(request, total=0, counter=0, cart_items=None):
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            counter += cart_item.quantity
    except ObjectDoesNotExist:
        pass
    return render(request, 'cart.html', dict(cart_items=cart_items, total=total, counter=counter))


def cart_remove(request, product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    products = get_object_or_404(product, id=product_id)
    cart_item = CartItem.objects.get(product=products, cart=cart)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart:cart_detail')


def full_remove(request, product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    products = get_object_or_404(product, id=product_id)
    cart_item = CartItem.objects.get(product=products, cart=cart)
    cart_item.delete()
    return redirect('cart:cart_detail')


def add_to_wishlist(request, product_id):
    product_instance = product.objects.get(pk=product_id)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    wishlist.products.add(product_instance)
    wishlist1 = Wishlist.objects.filter(user=request.user).first()
    wishlist_items = wishlist1.products.all() if wishlist else []
    print(wishlist_items)
    cart = Cart.objects.get(cart_id=_cart_id(request))
    cart_item = CartItem.objects.get(product_id=product_instance, cart=cart)
    cart_item.delete()
    return render(request, 'product_list.html', {'wishlist_items': wishlist_items})


@login_required
def remove_from_wishlist(request, product_id):
    product_instance = get_object_or_404(product, pk=product_id)

    wishlist_entry = Wishlist.objects.filter(user=request.user, products=product_instance).first()

    if wishlist_entry:
        wishlist_entry.delete()

    return redirect('cart:wishlist')


@login_required
def view_wishlist(request):
    wishlist = Wishlist.objects.filter(user=request.user).first()
    wishlist_items = wishlist.products.all() if wishlist else []
    return render(request, 'product_list.html', {'wishlist_items': wishlist_items})


@login_required
def wishlist(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)
    return render(request, 'product_list.html', {'wishlist_items': wishlist_items})
