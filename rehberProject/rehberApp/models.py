from django.db import models

class InfoOfArea(models.Model):
    name=models.CharField(max_length=200)
    imageUrl=models.TextField()
    description=models.TextField()
