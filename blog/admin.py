from django.contrib import admin
from .models import Post, Category # admin에 카테고리 등록해야 admin페이지에서 카테고리가 뜸

admin.site.register(Post)
admin.site.register(Category)

# Register your models here.
