from django.db import models


class Contact(models.Model):
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    phone =models.CharField(max_length=12)
    date=models.DateField()
    subject=models.TextField()
    message=models.TextField()