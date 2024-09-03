from django import template
from shop.models import Category, Product, Review
from orders.models import OrderItem, Order
from django.db.models import Sum
from django.utils import timezone
from datetime import timedelta

register = template.Library()

@register.inclusion_tag('shop/category/last_five_categories.xhtml')
def get_last_five_categories():
    categories = Category.objects.order_by('-id')[:5]
    return {'categories': categories}

@register.inclusion_tag('shop/product/latest_products.xhtml')
def get_latest_products():
    products = Product.objects.order_by('-id')[:6]
    return {'products': products}

@register.inclusion_tag('shop/product/best_seller.xhtml')
def get_best_seller_products():
# Get the top 3 best-selling products by quantity
    best_sellers = (
    OrderItem.objects.filter(order__paid=True)  # Filter for paid orders
    .values('product')  # Group by product
    .annotate(total_quantity_sold=Sum('quantity'))  # Sum the quantities sold
    .order_by('-total_quantity_sold')[:3]  # Order by total quantity sold, limit to top 3
)

    # Fetch the Product instances for the best-selling products
    product_ids = [seller['product'] for seller in best_sellers]
    products = Product.objects.filter(id__in=product_ids)
    ratings_bs = {}
    no_rate_bs = {}
    for product in products:
        # product = Product.objects.filter(id=product)
        rating = product.average_rating()
        if rating:
            ratings_bs[product.id] = int(rating)
            empty = 5-rating
            no_rate_bs[product.id] = int(empty)
    pros = sorted(products, key=lambda p: next(s['total_quantity_sold'] for s in best_sellers if s['product'] == p.id), reverse=True)
    # Return the products ordered by their sold quantities
    return {'best_sellers': pros, 'ratings_bs': ratings_bs, 'no_rate_bs': no_rate_bs}

# Get the top 3 popular 
@register.inclusion_tag('shop/product/top_new.xhtml')
def get_top_new_products():
    # Define the time range for new products
    time_threshold = timezone.now() - timedelta(days=365)
    recents = Product.objects.filter(created__gte=time_threshold)
    best_sellers = (
    OrderItem.objects.filter(order__paid=True, product__in=recents)  # Filter for paid orders and recent products
    .values('product')  # Group by product
    .annotate(total_quantity_sold=Sum('quantity'))  # Sum the quantities sold
    .order_by('-total_quantity_sold')[:3]  # Order by total quantity sold, limit to top 3
    )
    # Fetch the Product instances for the top-selling products
    product_ids = [seller['product'] for seller in best_sellers]
    top_new_products = Product.objects.filter(id__in=product_ids)
    ratings_tn = {}
    no_rate_tn = {}
    for product in top_new_products:
        rating = product.average_rating()
        if rating:
            ratings_tn[product.id] = int(rating)
            empty = 5-rating
            no_rate_tn[product.id] = int(empty)
        else:
            ratings_tn[product.id] = 0
            no_rate_tn[product.id] = 5
    top_new = sorted(top_new_products, key=lambda p: next(s['total_quantity_sold'] for s in best_sellers if s['product'] == p.id), reverse=True)
    # Return the products ordered by their sold quantities
    return { 'top_new': top_new, 'ratings_tn': ratings_tn, 'no_rate_tn': no_rate_tn}

@register.inclusion_tag('shop/product/recently_viewed.xhtml', takes_context=True)
def get_recently_viewed(context):
    request = context['request']
    recently_viewed_ids = request.session.get('recently_viewed', [])[:3]
    
    if not recently_viewed_ids:
        return {'recently_viewed_products': []}
        
    recently_viewed_products = Product.objects.filter(id__in=recently_viewed_ids)
    ratings = {}
    no_rate = {}
    for product in recently_viewed_products:
        # product = Product.objects.filter(id=product)
        rating = product.average_rating()
        if rating:
            ratings[product.id] = int(rating)
            empty = 5-rating
            no_rate[product.id] = int(empty)
    return {'recently_viewed_products': recently_viewed_products, 'ratings': ratings, 'no_rate': no_rate}
