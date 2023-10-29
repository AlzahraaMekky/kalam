from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from datetime import date
class CustomUser(AbstractUser):
    USER_CHOICES = (
    ("ADMIN", "1"),
    ("user", "2"),
    ("coffee", "3")

)

    userType = models.CharField(max_length=9,choices=USER_CHOICES)
    username = models.CharField(max_length = 50, blank = True, null = True, unique = True)
    Full_name = models.CharField(max_length = 200)
    phone_no = models.CharField(max_length = 10)
    Photo = models.ImageField(upload_to='profile/', blank=True)

    def __str__(self):
      return self.username
    

class Coffee(models.Model):
    name = models.CharField(max_length = 50)
    description = models.TextField()
    img = models.ImageField(upload_to='coffee/')
    address = models.CharField(max_length = 50)
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
   
    def __str__(self):
      return self.name
  
class CoffeeSesion(models.Model):
  SESSIN_CHOICES = (
    ("sport", "1"),
    ("culture", "2"),
    ("policy", "3")

  )
  name = models.CharField(max_length = 50)
  description = models.TextField()
  type = models.CharField(max_length=9,choices=SESSIN_CHOICES)
  datetime = models.DateTimeField(auto_now_add=True)
  img = models.ImageField(upload_to='coffee/')
  price= models.IntegerField()
  user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
  
  def __str__(self):
    # return f"{self.datetime.strftime('%d-%m-%Y')}"
    return self.name
  

class Booking(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    session = models.ForeignKey(CoffeeSesion,on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    message = models.TextField(null=True, blank=True)
    class Meta:
        ordering = ['-date']
