from django.shortcuts import render
from .models import Post

# Create your views here.

def index(request): # request는 기본이다.
    posts = Post.objects.all()
    return render(request, 'blog/index.html',{ 'posts' : posts,'a_plus_b' : 1+3})
    # request는 기본, 템플릿이 되는것을 넣어주기