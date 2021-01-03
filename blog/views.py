from django.shortcuts import render
from .models import Post
from django.views.generic import ListView
# Create your views here.

class PostList(ListView):
    model = Post
# django에서 제동하는 블로그 모듈, index를 이렇게 제공해줌
    def get_queryset(self):
        return Post.objects.order_by('-creaded')



def index(request): # request는 기본이다.
    posts = Post.objects.all()
    return render(request, 'blog/post_list.html', {'posts' : posts, 'a_plus_b' : 1 + 3})
    # ctrl 누르고 'blog/post_list.html' 을 누르면 해당 장소로 간다!
    # request는 기본, 템플릿이 되는것을 넣어주기


