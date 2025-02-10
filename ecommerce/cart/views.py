from lib2to3.fixes.fix_input import context

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
import razorpay
from decimal import Decimal

from cart.models import Cart, Payment, Order_details
from shop.models import Product


@login_required
def cart_view(request):
    cart_items = Cart.objects.filter(user=request.user)
    total = sum(item.product.price * item.quantity for item in cart_items)  # Fixed subtotal
    return render(request, 'cart.html', {'cart': cart_items, 'total': total})


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart:cart_view')


@login_required
def cart_decrement(request, product_id):
    cart_item = get_object_or_404(Cart, user=request.user, product_id=product_id)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart:cart_view')


@login_required
def cart_delete(request, product_id):
    cart_item = get_object_or_404(Cart, user=request.user, product_id=product_id)
    cart_item.delete()
    return redirect('cart:cart_view')


@login_required
def orderform(request):
    if request.method == "POST":
        address = request.POST.get('a', '')
        phone = request.POST.get('p', '')
        pin = request.POST.get('n', '')

        user = request.user
        cart_items = Cart.objects.filter(user=user)

        if not cart_items:
            return redirect('cart:cart_view')  # Redirect if cart is empty

        # Convert total to float to avoid JSON serialization error
        total = float(sum(item.product.price * item.quantity for item in cart_items))

        # Razorpay client connection
        client = razorpay.Client(auth=('rzp_test_9SsiNMi8rbxStO', 'TSNDFbpGltQsnOonO4jm7aj7'))

        # Razorpay order creation (convert amount to paise)
        response_payment = client.order.create(dict(amount=int(total * 100), currency='INR'))

        order_id = response_payment.get('id')
        status = response_payment.get('status')

        if status == "created":
            # Save Payment record
            payment = Payment.objects.create(name=user.username, amount=total, order_id=order_id, paid=False)

            # Save each cart item as an order
            for item in cart_items:
                Order_details.objects.create(
                    product=item.product, user=user, phone=phone, address=address,
                    pin=pin, order_id=order_id, no_of_items=item.quantity, payment_status="pending"
                )

            # Pass payment details to the template
            context = {'payment': response_payment, 'name': user.username}
            return render(request, 'payment.html', context)

    return render(request, 'orderform.html')


@csrf_exempt
def payment_status(request, username):
    try:
        # ✅ Retrieve the user based on username
        user = User.objects.get(username=username)
        login(request, user)

        # ✅ Razorpay response
        response = request.POST
        print(response)

        # ✅ Validate Razorpay payment signature
        param_dict = {
            'razorpay_order_id': response.get('razorpay_order_id'),
            'razorpay_payment_id': response.get('razorpay_payment_id'),
            'razorpay_signature': response.get('razorpay_signature'),
        }

        client = razorpay.Client(auth=('rzp_test_9SsiNMi8rbxStO', 'TSNDFbpGltQsnOonO4jm7aj7'))

        # ✅ Verify payment signature
        status = client.utility.verify_payment_signature(param_dict)

        if status:
            print("✅ Payment Verified")

            # ✅ Update Payment record
            payment = Payment.objects.get(order_id=response.get('razorpay_order_id'))
            payment.razorpay_payment_id = response.get('razorpay_payment_id')
            payment.paid = True
            payment.save()

            # ✅ Update Order details
            orders = Order_details.objects.filter(order_id=response.get('razorpay_order_id'))
            for order in orders:
                order.payment_status = "completed"
                order.save()

            # ✅ Remove cart items after successful payment
            Cart.objects.filter(user=user).delete()

            return render(request, 'payment_success.html')  # Redirect to success page

    except:
        pass
@login_required
def order_view(request):
    u=request.user
    o = Order_details.objects.filter(user=u,payment_status="completed")
    context={'orders':o}
    return render(request, 'order_view.html',context)

