from django.db import models
from django.urls import reverse
from shop.models import Product
from django.contrib.auth.models import User

# Create your models here.
class WishList(models.Model):
    user_id = models.ForeignKey(User, verbose_name=("user_wishlist"), on_delete=models.CASCADE)
    product_id = models.ManyToManyField(Product, verbose_name=("product_wishlist"))
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # class Meta:
    #     indexes = [
    #         models.Index(fields=['-created']),
    #     ]

    # def get_absolute_url(self):
    #     return reverse('shop:product_detail',
    #                    args=[self.id, self.slug])
    
    def __str__(self):
        return f"{self.user_id.username}'s Wishlist"
    