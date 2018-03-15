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
# from django.conf.urls import url
# from django.contrib import admin
# from demoapp.views import home
# from demoapp.views import example
# from demoapp.views import users
# from demoapp import views
#
# from django.views.generic import RedirectView
# from django.contrib.staticfiles.views import serve
#
# CORS_ORIGIN_ALLOW_ALL = True
#
# urlpatterns = [
#     #url(r'^$', home, name='home'),
#     url(r'^$', serve,kwargs={'path': 'index.html'}),
#     url(r'^(?!/?static/)(?!/?media/)(?P<path>.*\..*)$',
#     RedirectView.as_view(url='/static/%(path)s', permanent=False)),
#
#     #url(r'^api/login/(?P<email>\w{0,50})/(?P<password>\w{0,50})/$', views.login, name='login'),
#     url(r'^api/login/(?P<email>[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})/(?P<password>\w{0,50})/$', views.login, name='login'),
#
#     url(r'^api/users/(?P<user_id>\w{0,50})/(?P<firstname>\w{0,50})/(?P<lastname>\w{0,50})/(?P<username>\w{0,50})/(?P<password>\w{0,50})/(?P<email>[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})/(?P<birth_year>\w{0,50})/(?P<gender>\w{0,50})/$', users, name='users'),
#
#     url(r'^example/', example, name='example'),
#
#     url(r'^admin/', admin.site.urls),
# ]
