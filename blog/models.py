from django.db import models
from django.contrib.auth.models import User # 유저 개념
# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length = 30) # 블로그에서 글
    content = models.TextField() # 블로그 내용

    creaded = models.DateField() #언제 작성이 되는지

    author = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL) # 어떤 사용자가 사용이 되는지 유저라는 객체를 연결시켜줌
    # 누가 들어올 수 있다.
    #on_delate = True 사용자가 탈퇴를 할 때 글도 삭제할꺼냐?



