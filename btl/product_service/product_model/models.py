from django.db import models

# Create your models here.
class StoreHouse(models.Model):
    address = models.CharField(max_length=255,unique=True)
    
    def __str__(self):
        return self.address
    
class Category(models.Model):
    name = models.CharField(max_length=50,unique=True)
    
    def __str__(self):
        return self.name
    
class Suppliers(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=12)
    
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=50)
    image = models.CharField(max_length=255) 
    price = models.FloatField()
    amount = models.IntegerField()
    description = models.TextField()
    supplier = models.ForeignKey(Suppliers,on_delete=models.CASCADE)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    storehouse = models.ForeignKey(StoreHouse,on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name