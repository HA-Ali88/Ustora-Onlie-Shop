from shop import views
from django.urls import path

app_name = 'shop'
urlpatterns = [
    path('', views.home_page, name='home_page'),
    path('shop/', views.product_list, name='product_list'),
    path('categories/', views.category_list,
         name='category_list'),
    path('subscribe/', views.subscribe, name='subscribe'),
    path('topnew/', views.topnew_product_list, name='topnew_product_list'),
    path('best-sellers/', views.best_sellers_product_list, name='best_sellers_product_list'),
    path('recently-viewed/', views.recently_viewed_list, name='recently_viewed_list'),
    path('tag/<slug:tag_slug>/', views.product_by_slug, name='product_by_slug'),
    path('search/', views.search_by_name_desc, name='search_by_name_desc'),
    path('<slug:category_slug>/', views.product_list,
         name='product_list_by_category'),
    path('<int:id>/<slug:slug>/', views.product_detail,
         name='product_detail'),
]