from django.db import models
from django.core.urlresolvers import reverse
from datetime import datetime,timezone
from django.contrib.auth.models import User,Permission

class Album(models.Model):
    user = models.ForeignKey(User, default=1)
    artist = models.CharField(max_length=100)
    album_title = models.CharField(max_length=100)
    genre = models.CharField(max_length=100)
    album_logo = models.FileField()
    is_favorite = models.BooleanField(default=False)


    def get_absolute_url(self):
        return reverse('gaana:detail',kwargs={'pk':self.pk})

    def __str__(self):
        return self.album_title+'-'+self.artist

class Song(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    song_title = models.CharField(max_length=500)
    song_file = models.FileField(default=None)
    #date = models.DateTimeField(default=datetime.now)
    is_favorite = models.BooleanField(default=False)

    def __str__(self):
        return self.song_title

class Comment(models.Model):
    album = models.ForeignKey(Album,on_delete=models.CASCADE)
    obj_id = models.IntegerField(max_length=5)
    userdetail = models.CharField(max_length=200)
    content = models.TextField()
    created_date = models.DateTimeField(default=datetime.now)
    #approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.content


#class UserForm(models.User)
#can be inherited by using from django.contrib.auth.models import User