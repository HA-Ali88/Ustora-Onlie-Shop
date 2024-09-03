from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User
from wishlist.models import WishList
from shop.models import Product


# Create your views here.
@login_required
def add(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    user = get_object_or_404(User, pk=request.user)
    wishlist, created = WishList.objects.filter(user_id = request.user)
    # Add the product to the wishlist
    wishlist.product_id.add(product)
    # Save the wishlist (optional, since add() should handle it)
    wishlist.save()
    messages.success(request, 'Wishlist updated '\
                                      'successfully')
    return redirect('shop:product_list')

@login_required
def remove(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    user = get_object_or_404(User, pk=request.user)
    wishlist = get_object_or_404(WishList, user=request.user)
    wishlist.product_id.remove(product)
    messages.success(request, 'Wishlist updated '\
                                      'successfully')
    return redirect('/')

@login_required
def list(request):
    wishlist, created = WishList.objects.get_or_create(user_id = request.user)
    # products = wishlist.product_id.all()  # Retrieve all products in the wishlist
    # products = Product.objects.all() 
    # print(request.user.user_wishlist)
    products = wishlist.product_id.all() if wishlist else []
    page = request.GET.get('page', 1)
    paginator = Paginator(products, 2)
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    return render(request,
                  'wishlist/list.xhtml',
                  {'products': products})

@login_required
def toggle_wishlist(request, product_id):
    # if request.method == "POST":
        product = get_object_or_404(Product, id=product_id)
        wishlist, created = WishList.objects.get_or_create(user_id = request.user)
        if product in wishlist.product_id.all():
            wishlist.product_id.remove(product)
            action = 'removed'
        else:
            wishlist.product_id.add(product)
            action = 'added'
        return JsonResponse({'status': 'success', 'action': action})
    # return JsonResponse({'status': 'failed'}, status=400)
