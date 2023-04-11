from django.db import models

# Create your models here.
class contact(models.Model):
    name = models.CharField(max_length=90)
    email = models.EmailField(max_length=90)
    message = models.TextField()
    
class items(models.Model):
    Name = models.CharField(max_length=90)
    img_Link = models.CharField(max_length=200)
    user_id =  models.IntegerField()   