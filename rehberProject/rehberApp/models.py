from django.db import models

class InfoOfArea(models.Model):
    name=models.CharField(max_length=200)
    imageUrl=models.CharField(max_length=250)
    description=models.TextField()
