"""TheBlog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from blog import views as blog_views
from django_mfa import urls as tf_urls
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('settings/', include(tf_urls)),
    path('', include('blog.urls')),
    path('admin/', include('admin_honeypot.urls', namespace='admin_honeypot')),
    path('secret/', admin.site.urls),
    path('contact/', blog_views.contact_view, name='contact'),
    path('sessiontimeout/', blog_views.session_timeout_view, name='sessiontimeout'),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/',auth_views.LogoutView.as_view(), name='logout'),
    path('accounts/password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('accounts/password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('accounts/password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('accounts/reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('accounts/password-change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('accounts/password-change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('activate/<uidb64>/<token>/',blog_views.activate, name='activate'),
    path('signup/', blog_views.signup, name='signup'),
    path('captcha/', include('captcha.urls'), name='captcha'),
    path('profile/', blog_views.update_profile, name='profile'),
    path('about-us/', blog_views.about, name='about-us'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
