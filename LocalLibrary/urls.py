"""LocalLibrary URL Configuration

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
from django.contrib import admin
from django.conf.urls import include
from django.urls import path
from django.views.generic import RedirectView

# this is the primary entry point for the web site
# urlpatterns directs page requests to views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # this redirects to the admin views
    path('admin/', admin.site.urls),
    # this redirects to the catalog page views
    path('catalog/', include('catalog.urls')),
    # this redirects to the accounts page views
    path('accounts/', include('django.contrib.auth.urls')),
    # this is a catch all else that redirects to the catalog landing view
    path('', RedirectView.as_view(url='/catalog/')),
]

# code from tutorial didn't work, settings.STATIC_ROOT seems to have been depreciated
# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root='')
