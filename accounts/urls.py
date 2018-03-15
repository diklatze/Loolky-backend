"""loolky URL Configuration

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
from . import views

CORS_ORIGIN_ALLOW_ALL = True

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^signup/', views.user_signup, name='user_signup'),
    url(r'^signup_done/', views.user_signup_done, name='user_signup_done'),
    url(r'^user_update/', views.user_update, name='user_update'),
    url(r'^login/', views.user_login, name='user_login'),
    url(r'^logout/', views.user_logout, name='user_logout'),
    url(r'^change_password/', views.change_password, name='change_password'),
    url(r'^reset_password/', views.reset_password, name='reset_password')
]
