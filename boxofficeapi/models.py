from django.db import models

class Movie(models.Model):
    movieName = models.CharField(max_length=100)
    language = models.CharField(max_length=50)
    actors = models.CharField(max_length=200)  # comma separated list of actor names
    director = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    imageUrl = models.CharField(max_length=500)
    is_active = models.BooleanField(default=True)
    startDate=models.DateField()
    endDate=models.DateField()
    
    
class Ticket(models.Model):
    movie_id = models.IntegerField()
    movieName = models.CharField(max_length=100)
    date = models.DateField()
    time = models.CharField(max_length=100)
    seat_row = models.CharField(max_length=10)
    seat_number = models.CharField(max_length=10)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    username = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
   
    