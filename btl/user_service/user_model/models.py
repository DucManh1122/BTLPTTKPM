from django.db import models

# Create your models here.

from django.db import models
    
class Role(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Account(models.Model):
    username = models.CharField(max_length=50,unique=True)
    password = models.CharField(max_length=50)
    role = models.ForeignKey(Role,on_delete=models.CASCADE) 
    
    def __str__(self):
        return self.username

class UserInfo(models.Model):
    fname = models.CharField(max_length=50)
    lname = models.CharField(max_length=50)
    email = models.EmailField()
    phone_number = models.CharField(max_length=12)
    address = models.CharField(max_length=100)
    account = models.ForeignKey(Account,on_delete=models.CASCADE)
    def __str__(self):
        return self.address
    







