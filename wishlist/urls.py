
from django.urls import path, include, reverse_lazy
from wishlist import views

app_name = "wishlist"

urlpatterns = (
    # path('add/<int:product_id>', views.add, name='add'),
    # path('remove/<int:product_id>', views.remove, name='remove'),
    path('list/', views.list, name='list'),
    path('toggle/<int:product_id>/', views.toggle_wishlist, name='toggle_wishlist'),
    # path('register/', authviews.re.as_view(), name="register"),
    # path('test/', views.test, name="loginoo"),
)
