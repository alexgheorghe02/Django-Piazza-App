from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError

class WallPost(models.Model):
    topics = (
    ("Tech", "Tech"),
    ("Health", "Health"),
    ("Sport", "Sport"),
    ("Politics", "Politics"))

    owner = models.ForeignKey(User, on_delete = models.CASCADE)
    title = models.CharField(max_length=100)
    topic = models.CharField(max_length=20, choices = topics)
    body = models.TextField(max_length = 5000)
    post_time = models.DateTimeField(default = timezone.now)
    expiry_time = models.DateTimeField(blank=True)
    status = models.CharField(max_length = 10, default = 'Live')

    def save(self, *args, **kw):
        if self.expiry_time < timezone.now():
            self.status = 'Expired'
        super(WallPost, self).save(*args, **kw)
    
    @property
    def number_of_likes(self):
        return WallLike.objects.filter(blogpost=self).count()
    
    @property
    def number_of_dislikes(self):
        return WallDislike.objects.filter(blogpost=self).count()
    
    @property
    def number_of_comments(self):
        return WallComment.objects.filter(blogpost=self).count()
    
    @property
    def comments(self):
        list = []
        for entry in WallComment.objects.all():
            if entry.blogpost.id == self.id:
                list.append([entry.comment, 'written by: ' +  entry.author.username])
        return list
    
    @property
    def written_by(self):
        return self.owner.username
    
    @property
    def this_id(self):
        return self.id
    
    def __str__(self):
        return 'written by: ' + self.owner.username + ' subject: ' + self.title
    

    
class WallLike(models.Model):
    blogpost = models.ForeignKey(WallPost, on_delete = models.CASCADE)
    author = models.ForeignKey(User, on_delete = models.CASCADE)
    date_posted = models.DateTimeField(default = timezone.now)

    @property
    def liked_by(self):
        return self.author.username
    
    is_cleaned = False

    def clean(self):
        if self.author.id == self.blogpost.owner.id:
            raise ValidationError('You cannot like your own post!')
        elif self.date_posted > self.blogpost.expiry_time:
            raise ValidationError('This post is expired!')
        self.is_cleaned = True

    def save(self, *args, **kwargs):
        if not self.is_cleaned:
            self.clean()
        super().save(*args, **kwargs)


class WallDislike(models.Model):
    blogpost = models.ForeignKey(WallPost, on_delete = models.CASCADE)
    author = models.ForeignKey(User, on_delete = models.CASCADE)
    date_posted = models.DateTimeField(default = timezone.now)

    @property
    def disliked_by(self):
        return self.author.username
    
    is_cleaned = False
    
    def clean(self):
        if self.author.id == self.blogpost.owner.id:
            raise ValidationError('You cannot dislike your own post!')
        elif self.date_posted > self.blogpost.expiry_time:
            raise ValidationError('This post is expired!')
        self.is_cleaned = True

    def save(self, *args, **kwargs):
        if not self.is_cleaned:
            self.clean()
        super().save(*args, **kwargs)


class WallComment(models.Model):
    blogpost = models.ForeignKey(WallPost, on_delete = models.CASCADE)
    author = models.ForeignKey(User, on_delete = models.CASCADE)
    comment = models.TextField(max_length = 2000)
    date_posted = models.DateTimeField(default = timezone.now)

    @property
    def written_by(self):
        return self.author.username
    
    is_cleaned = False

    def clean(self):
        if self.date_posted > self.blogpost.expiry_time:
            raise ValidationError('This post is expired!')
        self.is_cleaned = True

    def save(self, *args, **kwargs):
        if not self.is_cleaned:
            self.clean()
        super().save(*args, **kwargs)


