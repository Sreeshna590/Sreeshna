from .models import Cart


def cart_context(request):
    cart_items = Cart.objects.all()  # Modify as per your cart logic
    cart_count = cart_items.count()  # Get total number of items in the cart

    return {
        'cart_items': cart_items,
        'cart_count': cart_count,
    }
