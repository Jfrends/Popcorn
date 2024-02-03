from django.db import models
from django.contrib.auth import get_user_model
import uuid

User = get_user_model()

# Create your models here.

    
class Movie(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    genres = models.TextField(max_length=150, default = "unknonwn")
    title = models.CharField(max_length=150)
    director = models.CharField(max_length=150)
    cast = models.CharField(max_length=150)
    ratings = models.CharField(max_length=20)
    poster = models.CharField(max_length=200)
    trailer_link = models.CharField(max_length=200)
    runtime = models.CharField(max_length=150)
    description = models.TextField(max_length=800)
    year = models.TextField(max_length=10, default="unknown")

    def __str__(self):
        return self.title

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_user = models.IntegerField()
    bio = models.TextField(max_length = 200, blank=True)
    profileimg = models.ImageField(upload_to='profile_images', default='blank_pfp.png')
    filmOn = models.IntegerField(default=0)
    numFilmsWatched = models.IntegerField(default=0)
    watchlist = models.ManyToManyField(Movie)

    def __str__(self):
        return self.user.username