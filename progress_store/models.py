from django.db import models
import datetime
from django.contrib.auth.models import User
# categories model
class Category(models.Model):
    name = models.CharField(max_length=100)
 

    
    def __str__(self) -> str:
        return self.name
    
    #@Dave Rob 2011 discovery
    class Meta:
        verbose_name_plural = 'categories'
    

# Customer details model    

class Customer(models.Model):
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    address = models.CharField(max_length=1000)
    phone = models.CharField(max_length=100)
    email = models.EmailField(max_length=250)
    password = models.CharField(max_length=1000)
    
    def __str__(self) -> str:
        return f"{self.firstname} {self.lastname}"

class CustomerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pics/', default='default.jpg')
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    email_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

# Products MOdel
class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=10000, default="", blank=True, null=True)
    price = models.DecimalField(max_digits=12, decimal_places=3, default=0)
    Category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    image = models.ImageField(upload_to='upload/product')
    is_sale = models.BooleanField(default=False)
    sale_price = models.DecimalField(default=0, decimal_places=2, max_digits=12)
    average_rating = models.FloatField(default=0.0) 
    

# Review model
class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE)
    rating = models.IntegerField(default=1)  # Star rating (1 to 5)
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    

# Customer Order Model
class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    address = models.CharField(max_length=1000, default="", blank=True, null=True)
    phone = models.CharField(max_length=12)
    date = models.DateField(default=datetime.datetime.today)
    email = models.EmailField(default="", max_length=1000)
    status = models.BooleanField(default=False)
