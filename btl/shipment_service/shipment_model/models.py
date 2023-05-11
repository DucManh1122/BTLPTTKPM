from django.db import models

# Create your models here.
class TypeShipment(models.Model):
    name = models.CharField(max_length=255,unique=True)
    
    def __str__(self):
        return self.name

class Shipment(models.Model):
    fromAddress = models.CharField(max_length=50)
    toAddress = models.CharField(max_length=255) 
    type_shipment = models.ForeignKey(TypeShipment,on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.fromAddress} {self.toAddress}'