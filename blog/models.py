from django.db import models
from django.contrib.auth.models import User # 유저 개념
# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=25, unique=True)
    description = models.TextField(blank=True) # 카테고리에 대한 설명을 쓸 수 있다. 중복을 방지하기 위해서  unique=True 사용

    slug = models.SlugField(unique=True, allow_unicode=True) # allow_unicode = 한글을 허용 적절하게 /이름/ 으로 만들어줌

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return '/blog/category/{}/'.format(self.slug)

    class Meta: # 이름 바꾸는 방법중 하나
        verbose_name_plural = 'categories'

class Tag(models.Model) :
    name = models.CharField(max_length=40, unique=True)
    slug = models.SlugField(unique=True, allow_unicode=True)

    def __str__(self):
        return self.name



class Post(models.Model):
    title = models.CharField(max_length = 30) # 블로그에서 글
    content = models.TextField() # 블로그 내용
    head_image = models.ImageField(upload_to='blog/%Y/%M/%d/',blank=True) # 년도를 넣게됨 Y 하면은 이미지 업로드 모듈
    creaded = models.DateField() #언제 작성이 되는지
    tags = models.ManyToManyField(Tag) # tag추가후 post에 추가


    author = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL) # 어떤 사용자가 사용이 되는지 유저라는 객체를 연결시켜줌

    category = models.ForeignKey(Category, blank=True, null=True,on_delete=models.SET_NULL)
    def __str__(self): # 오버라이딩 이 객체를 문자를 바꾸었을 때 어떻게 보여줄 것인지
        return '{}::{}'.format(self.title, self.author) # 제목 abc
    # 누가 들어올 수 있다.
    #on_delate = True 사용자가 탈퇴를 할 때 글도 삭제할꺼냐?

    def get_absolute_url(self): # 어드민 페이지에 view onsite 버튼이 생김
        return '/blog/{}/'.format(self.pk)
