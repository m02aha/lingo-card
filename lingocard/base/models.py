from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime
# Create your models here.

class User(AbstractUser):
    # pass
    name=models.CharField(max_length=200,null=True)
    email=models.EmailField(unique=True)
    

    # avatar=models.ImageField()

    USERNAME_FIELD='email'
    REQUIRED_FIELDS=[]



class Translation(models.Model):
    status_choices=[
        ("hard","hard"),
        ("medium","medium"),
    ("easy","easy")
    ]
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    original_txt=models.CharField(max_length=500)
    translated_txt=models.CharField(max_length=500)
    original_audio=models.FileField(upload_to='audio/original',blank=True,null=True)
    translated_audio=models.FileField(upload_to='audio/translated',blank=True,null=True)
    created=models.DateTimeField(auto_now_add=True)
   
    updated=models.DateTimeField(auto_now=True)
    status=models.CharField(max_length=6,choices=status_choices)
    prev_status=models.CharField(max_length=6,choices=status_choices)
    next_revision_date=models.DateTimeField()

    def __str__(self):
        return f"{self.original_txt}"
    class Meta:
        ordering=['-updated','-created']


