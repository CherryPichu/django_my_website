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

from django.urls import path, include # include 가져오기
from . import views

urlpatterns = [
    path('category/<str:slug>/', views.PostListByCategory.as_view()), # slug url 만들기
    path('tag/<str:slug>/', views.PostListByTag.as_view()), # slug url 만들기
    path('<int:pk>/update/', views.PostUpdate.as_view()), # <int:pk> int 타입으로 숫자가 들어올 때 pk를 의미한다.
    path('<int:pk>/', views.PostDetail.as_view()), # <int:pk> int 타입으로 숫자가 들어올 때 pk를 의미한다.
    path('create/', views.PostCreate.as_view()),
    # views의 post_detail를 실행시킨다.
    # 번호를 하나씩 부여한다.
    path('', views.PostList.as_view()),
]



