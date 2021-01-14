from django.contrib import admin
from .models import Post, Category, Tag # admin에 카테고리 등록해야 admin페이지에서 카테고리가 뜸

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug' : ('name', )} # slug을 자동으로 만들어주도록 정함

class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug' : ('name', )}
    
    
admin.site.register(Post)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)

# Register your models here.
