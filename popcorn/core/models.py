from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.
class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_user = models.IntegerField()
    bio = models.TextField(max_length = 200, blank=True)
    profileimg = models.ImageField(upload_to='profile_images', default='blank_pfp.png')
    numFilmsWatched = 0
    watchList = {}

    def __str__(self):
        return self.user.username
    
class Movie():
    genres = []
    title = ""
    director = ""
    cast = ""
    ratings = ""
    poster = ""
    trailer_link = ""
    runtime = ""

