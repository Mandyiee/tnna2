from django.db import models

# Create your models here.
class News(models.Model):
    title = models.CharField(null=True,blank=True,max_length=500)
    link = models.CharField(null=True,blank=True,max_length=500)
    imageLink = models.CharField(null=True,blank=True,max_length=500)
    excerpt = models.TextField(null=True,blank=True)
    date_posted = models.CharField(null=True,blank=True,max_length=500)
    site = models.CharField(null=True,blank=True,max_length=500)
    
    