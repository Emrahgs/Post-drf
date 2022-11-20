from django.contrib import admin
from .models import Category, Post

# Register your models here.

@admin.register(Post)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('title', 'id', 'status', 'slug', 'author')
    prepopulated_fields = {'slug': ('title',), }
    
admin.site.register(Category)
