"""sportsfeed URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.urls import path
from django.contrib import admin
from login import views as login_views
from home import views as home_views
from preferences import views as preferences_views

urlpatterns = [
    path('login/new/submit/', login_views.new_user_submit),
    path('login/new/', login_views.new_user),
    path('home/', home_views.home),
    path('login/submit/', login_views.login_submit),
    path('login/', login_views.login_user),
    path('admin/', admin.site.urls),
    path('user-preferences/<int:user_id>/',
        preferences_views.user_preferences),
]
