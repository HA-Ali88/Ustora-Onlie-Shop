from django.shortcuts import render, get_object_or_404, redirect
from shop.models import Category, Product, Subscriber
from django.core.paginator import Paginator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone
from datetime import timedelta
from django.db.models import Sum
from shop.recommender import Recommender
from wishlist.models import WishList
from orders.models import OrderItem
from django.db.models import Q
from django.contrib import messages
from django.core.mail import send_mail
from shop.forms import ReviewForm, SubscriptionForm

def home_page(request):
    categories = Category.objects.order_by('-id')[:4]
    return render(request, 'shop/index.html', {'section': 'home', 'categories': categories})

# Create your views here.
def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    # wishlist
    if request.user.is_authenticated:
        wishlist, created = WishList.objects.get_or_create(user_id = request.user)
        wishlst = wishlist.product_id.all() if wishlist else []
    else:
        wishlst = []
    if category_slug:
        language = request.LANGUAGE_CODE
        category = get_object_or_404(Category, translations__language_code=language,
                                      translations__slug=category_slug)
        products = products.filter(category=category)

    page = request.GET.get('page', 1)
    paginator = Paginator(products, 2)
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    return render(request,
                  'shop/product/list.xhtml',
                  {'category': category,
                   'categories': categories,
                   'products': products,
                   'section': 'list',
                   'wishlst': wishlst})

def product_detail(request, id, slug):
    language = request.LANGUAGE_CODE
    product = get_object_or_404(Product,
                                id=id, translations__language_code=language,
                                translations__slug=slug,
                                available=True)
    # Track recently viewed products
    recently_viewed = request.session.get('recently_viewed', [])
    if id not in recently_viewed:
        recently_viewed.insert(0, id)
        if len(recently_viewed) > 10:  # Limit to the most recent 10 products
            recently_viewed.pop()
    request.session['recently_viewed'] = recently_viewed
    r = Recommender()
    recommended_products = r.suggest_products_for([product], 4)
    recent_products = Product.objects.order_by('-created')[:5]
    current_cat = product.category
    five_products = Product.objects.filter(category=current_cat).exclude(id=product.id)[:5]
    # Review part get or create review
    reviews = product.reviews.all()
    average_rating = product.average_rating()
    if average_rating:
        average_rating_range = range(int(average_rating))
        no_rate = 5 - average_rating
        no_rating = range(int(no_rate))
    else:
        average_rating_range = 0
        no_rating = range(5)
    review_count = product.review_count()
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            if request.user.is_authenticated:
                review.name = request.user.email
            review.save()
            messages.success(request, "Your review has been saved successfully.")
            return redirect(f"{request.path}")
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
            return redirect(f"{request.path}")
    else:
        form = ReviewForm()
        
    return render(request,
                  'shop/product/detail.xhtml',
                  {'product': product,
                   'section': 'detail',
                   'recommended_products': recommended_products,
                   'recent_products': recent_products,
                   'Cproducts': five_products,
                   'reviews': reviews,
                   'average_rating_range': average_rating_range,
                   'no_rating': no_rating,
                   'review_count': review_count,
                   'form': form})

def category_list(request):
    categories = Category.objects.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(categories, 2)
    try:
        categories = paginator.page(page)
    except PageNotAnInteger:
        categories = paginator.page(1)
    except EmptyPage:
        categories = paginator.page(paginator.num_pages)
    return render(request,
                  'shop/category/list.xhtml',
                  {'categories': categories,
                   'section': 'category'})

def topnew_product_list(request):
    # wishlist
    if request.user.is_authenticated:
        wishlist, created = WishList.objects.get_or_create(user_id = request.user)
        wishlst = wishlist.product_id.all() if wishlist else []
    else:
        wishlst = []
    products = Product.objects.filter(available=True)
    # Define the time range for new products
    time_threshold = timezone.now() - timedelta(days=365)
    recents = Product.objects.filter(created__gte=time_threshold)
    best_sellers = (
    OrderItem.objects.filter(order__paid=True, product__in=recents)  # Filter for paid orders and recent products
    .values('product')  # Group by product
    .annotate(total_quantity_sold=Sum('quantity'))  # Sum the quantities sold
    .order_by('-total_quantity_sold')  # Order by total quantity sold
    )
    # Fetch the Product instances for the top-selling products
    product_ids = [seller['product'] for seller in best_sellers]
    top_new_products = Product.objects.filter(id__in=product_ids)
    tn =  sorted(top_new_products, key=lambda p: next(s['total_quantity_sold'] for s in best_sellers if s['product'] == p.id), reverse=True)
    # Return the products ordered by their sold quantities
    page = request.GET.get('page', 1)
    paginator = Paginator(tn, 2)
    try:
        tn = paginator.page(page)
    except PageNotAnInteger:
        tn = paginator.page(1)
    except EmptyPage:
        tn = paginator.page(paginator.num_pages)
    categories = Category.objects.order_by('-id')[:4]
    return render(request,
                  'shop/product/list.xhtml',
                  {'categories': categories,
                   'products': tn,
                   'section': 'list',
                   'wishlst': wishlst})

def best_sellers_product_list(request):
    if request.user.is_authenticated:
        wishlist, created = WishList.objects.get_or_create(user_id = request.user)
        wishlst = wishlist.product_id.all() if wishlist else []
    else:
        wishlst = []
    # Get the top all best-selling products by quantity
    best_sellers = (
    OrderItem.objects.filter(order__paid=True)  # Filter for paid orders
    .values('product')  # Group by product
    .annotate(total_quantity_sold=Sum('quantity'))  # Sum the quantities sold
    .order_by('-total_quantity_sold')  # Order by total quantity sold, limit to top all
)

    # Fetch the Product instances for the best-selling products
    product_ids = [seller['product'] for seller in best_sellers]
    products = Product.objects.filter(id__in=product_ids)
    pros = sorted(products, key=lambda p: next(s['total_quantity_sold'] for s in best_sellers if s['product'] == p.id), reverse=True)
    page = request.GET.get('page', 1)
    paginator = Paginator(pros, 2)
    try:
        pros = paginator.page(page)
    except PageNotAnInteger:
        pros = paginator.page(1)
    except EmptyPage:
        pros = paginator.page(paginator.num_pages)
    categories = Category.objects.order_by('-id')[:4]
    return render(request,
                  'shop/product/list.xhtml',
                  {'categories': categories,
                   'products': pros,
                   'section': 'list',
                   'wishlst': wishlst})

def recently_viewed_list(request):
    if request.user.is_authenticated:
        wishlist, created = WishList.objects.get_or_create(user_id=request.user)
        wishlst = wishlist.product_id.all() if wishlist else []
    else:
        wishlst = []
    recently_viewed_ids = request.session.get('recently_viewed', [])
    if not recently_viewed_ids:
        recently_viewed_products = []
    else:
        recently_viewed_products = Product.objects.filter(id__in=recently_viewed_ids)
        page = request.GET.get('page', 1)
        paginator = Paginator(recently_viewed_products, 4)
        try:
            recently_viewed_products = paginator.page(page)
        except PageNotAnInteger:
            recently_viewed_products = paginator.page(1)
        except EmptyPage:
            recently_viewed_products = paginator.page(paginator.num_pages)
    categories = Category.objects.order_by('-id')[:4]
    return render(request,
                  'shop/product/list.xhtml',
                  {'categories': categories,
                   'products': recently_viewed_products,
                   'section': 'list',
                   'wishlst': wishlst})
    
def product_by_slug(request, tag_slug):
    if request.user.is_authenticated:
        wishlist, created = WishList.objects.get_or_create(user_id=request.user)
        wishlst = wishlist.product_id.all() if wishlist else []
    else:
        wishlst = []
    products_by_slug = Product.objects.filter(tags__slug__in=[tag_slug])
    if not products_by_slug:
        products = []
    else:
        products = Product.objects.filter(id__in=products_by_slug)
        page = request.GET.get('page', 1)
        paginator = Paginator(products, 4)
        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)
    categories = Category.objects.order_by('-id')[:4]
    return render(request,
                  'shop/product/list.xhtml',
                  {'categories': categories,
                   'products': products,
                   'section': 'list',
                   'wishlst': wishlst})
    
def search_by_name_desc(request):
    if request.user.is_authenticated:
        wishlist, created = WishList.objects.get_or_create(user_id=request.user)
        wishlst = wishlist.product_id.all() if wishlist else []
    else:
        wishlst = []
    query = request.GET.get("search_term")
    if query:
        products_by_name = Product.objects.filter(Q(translations__name__icontains=query) | Q(translations__description__icontains=query))
    else:
        products_by_name = Product.objects.all()
    print(query, products_by_name)
    if not products_by_name:
        products = []
    else:
        products = Product.objects.filter(id__in=products_by_name)
        page = request.GET.get('page', 1)
        paginator = Paginator(products, 4)
        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)
    categories = Category.objects.order_by('-id')[:4]
    return render(request,
                  'shop/product/list.xhtml',
                  {'categories': categories,
                   'products': products,
                   'section': 'list',
                   'wishlst': wishlst})
    
def subscribe(request):
    if request.method == "POST":
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "You have successfully subscribed!")
            return redirect(f"shop:home_page")
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
            return redirect(f"shop:home_page")
    else:
        form = SubscriptionForm()

    return redirect(f"shop:home_page")

def send_newsletter(subject, message):
    subscribers = Subscriber.objects.all()
    for subscriber in subscribers:
        send_mail(
            subject,
            message,
            'from@example.com',
            [subscriber.email],
            fail_silently=False,
        )