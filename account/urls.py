
from django.urls import path, include, reverse_lazy
from django.contrib.auth import views as auth_views
from account import views

app_name = "account"

urlpatterns = (
    # path('login/', authviews.LoginView.as_view(template_name='registration/login.html'), name='login'),
    # path('logout/', authviews.LogoutView.as_view(template_name='registration/logged_out.html'), name='logout'),
    path('password_change/', views.CustomPasswordChangeView.as_view(), name='password_change_done'),
    path('password_reset/', views.CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('', include('django.contrib.auth.urls')),
    path('register/', views.register, name='register'),
    path('edit/', views.edit, name='edit'),
    path('users/', views.user_list, name='user_list'),
    path('users/<str:username>/', views.user_detail, name='user_detail'),
    # path('register/', authviews.re.as_view(), name="register"),
    path('test/', views.test, name="loginoo"),
)
