from django.db import models

# Create your models here.

class Cart(models.Model):
    username = models.CharField(max_length=50)
    product_id = models.IntegerField()
    quantity = models.IntegerField()

    def __str__(self):
        return f'{self.username} {self.product_id} {self.category_product} {self.quantity}'