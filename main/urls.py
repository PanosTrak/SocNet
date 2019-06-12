"""SocNet URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.homepage_view, name='homepage'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='register'),
    path('register/', views.register_view, name='register'),
    path('profile/', views.redirect_to_current_profile, name='redirect_to_current_profile'),
    path('profile/<username>/', views.profile_view, name='profile'),
    path('search_profile/', views.search_profile, name='profile_profile'),
    path('settings/', views.settings, name='settings'),
    path('settings/profile/', views.profile_settings, name='profile_settings'),
    path('settings/account/', views.account_settings, name='account_settings'),
]
