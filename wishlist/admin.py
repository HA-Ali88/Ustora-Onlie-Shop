from django.contrib import admin
from wishlist.models import WishList

# Register your models here.
@admin.register(WishList)
class WishListAdmin(admin.ModelAdmin):
    list_display = ["id", "user_id", "created", "updated"]
