from django.db import models
from django.contrib.auth.models import User
    
class Bak(models.Model):
    CHOICES = (
        ('NN', 'none'),
	    ('HB', 'hangbu'),
        ('HBM', 'hangbumem'),
        ('IB', 'ibbu'),
        ('IBM', 'ibbumem'),
        ('GB', 'gambu'),
        ('GBM', 'gambumem'),
  )
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    money = models.IntegerField(default='400')
    work = models.CharField(max_length=3, choices=CHOICES, null=True)

    def __str__(self):
        return self.user.username

# Create your models here.
