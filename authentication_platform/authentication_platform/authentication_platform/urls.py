"""authentication_platform URL Configuration

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
from django.conf.urls import include, url

urlpatterns = [
    url(r'^auth_code_manage/', include('auth_code_manage.urls')),
    url(r'^enterprise_manage/', include('enterprise_manage.urls')),
    url(r'^product_manage/', include('product_manage.urls')),
    url(r'^system_manage/', include('system_manage.urls')),
    url(r'^user_manage/', include('user_manage.urls')),
]
