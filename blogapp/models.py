from django.db import models
from django.contrib.auth.models import User
from profanity.validators import validate_is_profane

class Category(models.Model):
    cname = models.CharField(max_length=25)
    users = models.ManyToManyField('auth.User',related_name='Subscribed_Users')
    def __str__(self):
        return self.cname


class Post(models.Model):
    title = models.CharField(max_length=50 , unique=True)
    post_pic = models.ImageField(null=True, blank=True , upload_to ='blogapp/static/images/')
    content = models.TextField(max_length=1000,validators=[validate_is_profane])
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    createdAt = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete= models.CASCADE)
    Tag = models.CharField(max_length = 50 , null=True)
    def __str__(self):
        return self.title
    class Meta:
    # sort posts in chronological order by default
        ordering = ('-createdAt',)

class Comment(models.Model):
    #comment is deleted if either user was deleted or post was deleted
    commented_by = models.ForeignKey(User,on_delete = models.CASCADE)
    createdAt = models.DateTimeField(auto_now_add=True)
    bodytext = models.TextField(null = False,validators=[validate_is_profane])
    post_id = models.ForeignKey(Post , on_delete=models.CASCADE)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies',on_delete=models.CASCADE)
    
    class Meta:
        # sort comments in chronological order by default
        ordering = ('createdAt',)

    def __str__(self):
        return self.bodytext
   

    def __children__(self):
        return Comment.objects.filter(parent=self)
    

class Likes(models.Model):
    post_id = models.ForeignKey(Post,on_delete=models.CASCADE)
    liker_id = models.ForeignKey(User,on_delete=models.CASCADE)
    like_or_dislike = models.BooleanField(null=True)
    def define_reaction(self):
        return self.like_or_dislike
    define_reaction.short_description = "Like"
    define_reaction.boolean = True
    # This to prevent liking and disliking the post at the same time 
    class Meta:
        unique_together = ('post_id','liker_id')