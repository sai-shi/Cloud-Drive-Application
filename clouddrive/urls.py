"""clouddrive URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.contrib import admin, admindocs
from django.urls import path
from django.conf.urls import include, url
from django.contrib.auth import views as auth_views
from myApp.views import home, register_view, profile_view, \
    upload_view, logout_view, delete_view, process, detail_view

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('', home, name='home'),
    path('register/', register_view, name='register'),
    path('profile/', profile_view, name='profile'),
    path('upload/', upload_view, name='upload'),
    path('logout/', logout_view, name='logout'),
    path('delete/<username>/<filename>', delete_view, name='delete'),
    path('media/<username>/<filename>', detail_view, name='detail'),
    path('admin/doc/', include('django.contrib.admindocs.urls')),
    path('process/', process, name='process'),
    path('password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
