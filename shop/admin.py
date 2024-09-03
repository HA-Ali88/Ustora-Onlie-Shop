from django.contrib import admin
from parler.admin import TranslatableAdmin
from .models import Category, Product, Review, Subscriber
@admin.register(Category)
class CategoryAdmin(TranslatableAdmin):
    list_display = ['name', 'slug']
    def get_prepopulated_fields(self, request, obj=None):
        return {'slug': ('name',)}
@admin.register(Product)
class ProductAdmin(TranslatableAdmin):
    list_display = ['id', 'name', 'slug', 'price',
                    'available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated', 'tags']
    list_editable = ['price', 'available']
    def get_prepopulated_fields(self, request, obj=None):
        return {'slug': ('name',)}
@admin.register(Review)
class ReviewAdmin(TranslatableAdmin):
    list_display = ['product', 'email', 'rating', 'created_at']
    list_filter = ['product', 'rating']
    
@admin.register(Subscriber)
class SubscriberAdmin(TranslatableAdmin):
    list_display = ['email', 'date_subscribed']