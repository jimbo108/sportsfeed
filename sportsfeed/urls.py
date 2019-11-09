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
from django.contrib import admin
from login import views as login_views
from home import views as home_views

urlpatterns = [
    url(r'^login/new/submit/', login_views.new_user_submit),
    url(r'^login/new/', login_views.new_user),
    url(r'^home/', home_views.home),
    url(r'^login/submit/', login_views.login_submit),
    url(r'^login/', login_views.login_user),
    url(r'^admin/', admin.site.urls),
    url(r'^login/new/registerPreferences/', login_views.register_preferences)
]
