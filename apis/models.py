from datetime import datetime

from django.db import models


class User(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    password = models.CharField(max_length=200)
    no_of_follower = models.IntegerField(default=0)
    no_of_following = models.IntegerField(default=0)
    
    def __str__(self):
        return self.name
    
class Follow(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    followedBy = models.ManyToManyField(User,related_name='UserFollowers')
    following = models.ManyToManyField(User,related_name='whomuserfollowing')
    

class Post(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_time = models.DateField(default=datetime.now())
    number_of_comments = models.IntegerField(default=0)
    number_of_likes = models.IntegerField(default=0)

    def __str__(self):
        return self.title

class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    likedBy = models.ManyToManyField(User)
    

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    comment_body = models.TextField()
    created_time = models.DateField(default=datetime.now())


