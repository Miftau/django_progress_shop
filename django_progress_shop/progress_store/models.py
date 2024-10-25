from django.db import models
import datetime

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=10000, default="", blank=True, null=True)
    
    def __str__(self) -> str:
        return f"{self.name} \n {self.description}"
    
    
class Customer(models.Models):
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    address = models.CharField(max_length=1000)
    phone = models.CharField(max_length=100)
    email = models.EmailField(max_length=250)
    password = models.CharField(max_length=1000)
    
    def __str__(self) -> str:
        return f"{self.firstname} {self.lastname}"
    

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=10000, default="", blank=True, null=True)
    price = models.DecimalField(max_digits=12, decimal_places=3, default=0)
    Category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    image = models.ImageField(upload_to='/upload/product')
