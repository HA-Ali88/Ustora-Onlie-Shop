from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.contrib import messages
import weasyprint
from .models import OrderItem, Order
from .forms import OrderCreateForm, ContactForm
from cart.cart import Cart
from orders.tasks import order_created
from coupons.forms import CouponApplyForm
import time
def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = cart.coupon.discount
            order.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            # clear the cart
            cart.clear()
            # launch asynchronous task
            result = order_created.delay(order.id)
            # at this time, our task is not finished, so it will return False
            # print('Task finished? ', result.ready())
            # print('Task result: ', result.result)
            # # sleep 10 seconds to ensure the task has been finished
            # time.sleep(10)
            # # now the task should be finished and ready method will return True
            # print('Task finished? ', result.ready())
            # print('Task result: ', result.result)
            # set the order in the session
            request.session['order_id'] = order.id
            # redirect for payment
            return redirect(reverse('payment:process'))
        else:
            # Add a message to notify the user
            # Log and collect form errors
            error_messages = []
            for field, errors in form.errors.items():
                for error in errors:
                    error_message = f"Error in {field}: {error}"
                    error_messages.append(error_message)

            # Add a message to notify the user
            for error_message in error_messages:
                messages.error(request, error_message)
    else:
        form = OrderCreateForm()
    coupon_apply_form = CouponApplyForm()
    return render(request,
                  'orders/order/create.xhtml',
                  {'cart': cart, 'form': form, 'section': 'checkout', 'coupon_apply_form': coupon_apply_form})

@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request,
                  'admin/orders/order/detail.xhtml',
                  {'order': order})

@staff_member_required
def admin_order_pdf(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    html = render_to_string('orders/order/pdf.xhtml',
                            {'order': order})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=order_{order.id}.pdf'
    weasyprint.HTML(string=html).write_pdf(response,
        stylesheets=[weasyprint.CSS(settings.STATIC_ROOT / 'css/pdf.css')])
    return response

def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your message has been sent successfully.")
            return redirect('orders:contact')  # Use redirect to prevent form resubmission
        else:
            # Collect form errors
            error_messages = []
            for field, errors in form.errors.items():
                for error in errors:
                    error_message = f"Error in {field}: {error}"
                    error_messages.append(error_message)

            # Add error messages to the messages framework
            for error_message in error_messages:
                messages.error(request, error_message)
            
            # Render the form with the user's input and error messages
            return render(request, 'orders/order/contact.xhtml', {'form': form, 'section': 'contact'})
    else:
        form = ContactForm()
        return render(request, 'orders/order/contact.xhtml',  {'form': form, 'section': 'contact'})