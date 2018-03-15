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
    #url(r'^signup/(\d+)/(\d+)/(\d+)/(\d+)/(\d+)/', views.user_signup, name='user_signup'),
    url(r'^signup/(?P<username>[\w\-]+)/(?P<first_name>[\w\-]+)/(?P<last_name>[\w\-]+)/(?P<password>[\w\-]+)/(?P<email>[\w\-]+)/', views.user_signup, name='user_signup'),
    url(r'^update_user/', views.user_update, name='user_update'),
    url(r'^delete_user/', views.user_delete, name='user_delete'),
    url(r'^login/', views.user_login, name='user_login'),
    url(r'^logout/', views.user_logout, name='user_logout'),
    url(r'^password_change/', views.password_change, name='password_change'),
    url(r'^password_reset/', views.password_reset, name='password_reset')
]
