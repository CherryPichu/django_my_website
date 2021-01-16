"""my_site_prj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path, include # include 가져오기
from django.conf.urls.static import static # url 모음을 위한 추가
from django.conf import settings # url 모음을 위한 추가2

urlpatterns = [
    path('blog/', include('blog.urls')), # 이 blog로 왔을 때 blog.urls 로 가라
    path('admin/', admin.site.urls),
    path('markdownx/', include('markdownx.urls')), # url이 아니라 path로 사용 가능
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
