from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    first_name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to="media", blank=True, null=True)
    home = models.CharField(max_length=100, blank=True)
    profpic = models.ImageField(upload_to="media", default="/media/defaultprofpic.png")

class Trip(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="creator")
    title = models.TextField(max_length=500)
    location = models.CharField(max_length=100)
    timestamp = models.CharField(max_length=25)
    budget = models.CharField(max_length=5)
    plans = models.TextField()
    status = models.CharField(max_length=10)
    img = models.ImageField(upload_to="media", default="/media/default.png")
   
    def __str__(self):
        return f"{self.title}"

class Tag(models.Model):
    tags = models.CharField(max_length=50)
    trips = models.ManyToManyField(Trip, blank=True, related_name="trips")

    def __str__(self):
        return f"{self.tags}"

class List(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    lists = models.CharField(max_length=50)
    trips = models.ManyToManyField(Trip, blank=True, related_name="savedTrips")

    def __str__(self):
        return f"{self.lists}"

class Photo(models.Model):
    photos = models.ImageField(upload_to="media")
    caption = models.CharField(max_length=255, default="", blank=True)
    trips = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name="trip")