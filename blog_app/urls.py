
from django.contrib import admin
from django.urls import path,include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('my_site.urls')),
    path('accounts/logout', auth_views.LogoutView.as_view(template_name='registration/logged_out.html'), name='logout'),
    path('accounts/login', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
]
