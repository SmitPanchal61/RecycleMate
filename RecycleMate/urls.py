"""RecycleMate URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import include, path
# from django.contrib.staticfiles.urls import staticfiles_urlpatterns
# from RM import views
# from RM.views import index
from django.conf import settings  
from django.conf.urls.static import static 

urlpatterns = [
    # path('',index , name='index'), # front page hai toh empty
    path('admin/', admin.site.urls),
    path('', include('RM.urls')),
    # path('',views.index),
    # path('Signup',views.Signup),
    
    # path('RM/', include('RM.urls'))
] # + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# urlpatterns += staticfiles_urlpatterns()
if settings.DEBUG:  
        urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT) 