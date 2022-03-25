"""dispatcher URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from argparse import Namespace
from django.contrib import admin
from django.urls import path,include 
from rest_framework import routers
from apis import views as apisviews
from r2p import views as r2pviews 

router = routers.DefaultRouter()
router.register(r'users', apisviews.UserViewSet)
router.register(r'groups', apisviews.GroupViewSet)
# router.register(r'personsDetail', r2pviews.PersonsDetail, basename='personsDetail')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('r2p/', include('r2p.urls', namespace='r2p')),
    path('apis/', include('apis.urls', namespace='apis')) , 
    path('accounts/', include('accounts.urls')), # new
    path('accounts/', include('django.contrib.auth.urls'))
   
]
