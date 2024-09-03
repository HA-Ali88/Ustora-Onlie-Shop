from django.db import models
from django.urls import reverse
from parler.models import TranslatableModel, TranslatedFields
from taggit.managers import TaggableManager
from django.contrib.auth.models import User

# Create your models here.
class Category(TranslatableModel):
    translations = TranslatedFields(
    name = models.CharField(max_length=200),
    slug = models.SlugField(max_length=200,
                            unique=True),
    )
    image = models.ImageField(upload_to='categories/%Y/%m/%d',
                              blank=True)
    class Meta:
        # ordering = ['name']
        # indexes = [
        #     models.Index(fields=['name']),
        # ]
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def get_absolute_url(self):
        return reverse('shop:product_list_by_category',
                       args=[self.slug])
    
    def __str__(self):
        return self.name
    
class Product(TranslatableModel):
    category = models.ForeignKey(Category,
                                 related_name='products',
                                 on_delete=models.CASCADE)
    translations = TranslatedFields(
        name = models.CharField(max_length=200),
        slug = models.SlugField(max_length=200),
        description = models.TextField(blank=True),
    )
    image = models.ImageField(upload_to='products/%Y/%m/%d',
                              blank=True)
    price = models.DecimalField(max_digits=10,
                                decimal_places=2)
    tags = TaggableManager()
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    class Meta:
        # ordering = ['name']
        indexes = [
            # models.Index(fields=['id', 'slug']),
            # models.Index(fields=['name']),
            models.Index(fields=['-created']),
        ]

    def get_absolute_url(self):
        return reverse('shop:product_detail',
                       args=[self.id, self.slug])
    
    def __str__(self):
        return self.name
    
    def average_rating(self):
        return self.reviews.aggregate(models.Avg('rating'))['rating__avg']

    def review_count(self):
        return self.reviews.count()

class Review(models.Model):
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    email = models.EmailField()
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])  # Rating between 1 and 5
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('product', 'user')  # One review per user per product

    def __str__(self):
        return f'{self.product.name} - {self.user.username}'

class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    date_subscribed = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.email
