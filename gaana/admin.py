from django.contrib import admin

# Register your models here.
from .models import Album,Song,Comment
admin.site.register(Album)
admin.site.register(Song)
admin.site.register(Comment)
#can add any class to be appear and controled on admin page(site)
