from django.db import models

# Create your models here.

class Comment(models.Model):
    username = models.CharField(max_length=255)
    product_id = models.IntegerField()
    content = models.TextField()
    createAt = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.username} {self.content} {self.date}'
