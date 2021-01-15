from django.shortcuts import render
from .models import Post , Category, Tag
from django.views.generic import ListView, DetailView


# Create your views here.

class PostList(ListView):
    model = Post
# django에서 제동하는 블로그 모듈, index를 이렇게 제공해줌
    def get_queryset(self):
        return Post.objects.order_by('-creaded')

    def get_context_data(self, *, object_list=None, **kwargs): # 미리 만들어줌. 새로운 인자
        context = super(PostList, self).get_context_data(**kwargs) # 그량 외우기 복사 붙어넣기로
        context['category_list'] = Category.objects.all() # html에 category_list 변수가 생긴다.
        context['posts_without_category'] = Post.objects.filter(category=None).count() #get은 하나 filter는 특정 조건 all은 전부 #
        #category가 없는 것만 가져오기 이름이 posts_without_categor 이다 즉 object를 안서도 됨

        return context

def index(request): # request는 기본이다.
    posts = Post.objects.all()
    return render(request, 'blog/post_list.html', {'posts' : posts, 'a_plus_b' : 1 + 3})
    # ctrl 누르고 'blog/post_list.html' 을 누르면 해당 장소로 간다!
    # request는 기본, 템플릿이 되는것을 넣어주기

# def post_detail(request, pk):
#     blog_post = Post.objects.get(pk = pk) # 하나만 가져올 때 get, 전부는 all
#     return render(
#         request,
#         'blog/post_detail.html',
#         {
#             'blog_post' : blog_post # blog_post를 넘겨줌
#         }
#     ) # 및으로 요약 가능 이미 만들어진 기능임.
class PostDetail(DetailView):
    model = Post

    def get_context_data(self, *, object_list=None, **kwargs): # 미리 만들어줌. 새로운 인자
        context = super(PostDetail, self).get_context_data(**kwargs) # 그량 외우기 복사 붙어넣기로 자기 자신을 클래스에 넣기
        context['category_list'] = Category.objects.all() # html에 category_list 변수가 생긴다.
        context['posts_without_category'] = Post.objects.filter(category=None).count() #get은 하나 filter는 특정 조건 all은 전부 #
        #category가 없는 것만 가져오기 이름이 posts_without_categor 이다 즉 object를 안서도 됨
        return context

class PostListByTag(ListView):
    def get_queryset(self):
        tag_slug = self.kwargs['slug']
        tag = Tag.objects.get(slug=tag_slug)

        return tag.post_set.order_by('-creaded')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostListByTag, self).get_context_data(**kwargs)
        context['category_list'] = Category.objects.all()
        tag_slug = self.kwargs['slug']
        context['tag'] = Tag.objects.get(slug=tag_slug)
        return context

class PostListByCategory(ListView):
    def get_queryset(self):
        slug = self.kwargs['slug']

        if slug == '_none': # 미분류르 넣기 위한 방법
            category = None
        else :
            category = Category.objects.get(slug=slug)

        return Post.objects.filter(category=category).order_by('-creaded')

    def get_context_data(self, *, object_list=None, **kwargs): # 미리 만들어줌. 새로운 인자
        context = super(type(self), self).get_context_data(**kwargs) # 그량 외우기 복사 붙어넣기로
        context['category_list'] = Category.objects.all() # html에 category_list 변수가 생긴다.
        context['posts_without_category'] = Post.objects.filter(category=None).count() #get은 하나 filter는 특정 조건 all은 전부 #
        #category가 없는 것만 가져오기 이름이 posts_without_categor 이다 즉 object를 안서도 됨


        slug = self.kwargs['slug']
        if slug == '_none': # 미분류르 넣기 위한 방법
            category = None
            context['category']= "미분류"
        else :
            category = Category.objects.get(slug=slug)
            context['category'] = category

        # context['title'] = "Blog - {}".format(category.name)
        return context
# def index(request):
#     posts = Post.objects.all()
#     return  render(
#         request,
#         'blog/index.html',
#         {
#             'posts' : posts,
#         }
#     )