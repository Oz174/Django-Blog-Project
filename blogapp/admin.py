from django.contrib import admin
from .models import Post,Comment,Category,Likes
# Register your models here.

admin.site.site_header = "Django Blog"

class InjectComments(admin.StackedInline):
    model = Comment
    extra = 1

class InjectLikes(admin.StackedInline):
    model = Likes

class PostCustom(admin.ModelAdmin):
    
    fieldsets =(
        ['Post Info',{'fields': ['title','author','category','post_pic']}],
        ['Post Content',{'fields': ['content']}],
        ['Extra Info',{'fields':['Tag']}]
    )
    
    list_display = ("id","title","author","category")
    list_filter = ["category","author","title","createdAt"]
    search_fields = ["Tag", "category__cname"]
    inlines = [InjectComments,InjectLikes]

class InjectPost(admin.StackedInline):
    model = Post
    extra = 1

class CategoryCustom(admin.ModelAdmin):
    inlines = [InjectPost]

class LikesCustom(admin.ModelAdmin):
    list_display = ("post_id","liker_id","like_or_dislike")

class CommentCustom(admin.ModelAdmin):
    list_display = ("id","post_id","commented_by")

admin.site.register(Post,PostCustom)
admin.site.register(Category,CategoryCustom)
admin.site.register(Likes, LikesCustom)
admin.site.register(Comment, CommentCustom)