from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name

class Product(models.Model):
    title = models.CharField(max_length=30)
    amount = models.IntegerField()
    details = models.CharField(max_length=2000)
    image = models.ImageField(upload_to='picture',null=True,blank=True)
    ctry = models.ForeignKey(Category,on_delete=models.CASCADE, null=True, blank=True)
    us = models.ForeignKey(User,on_delete=models.CASCADE, null=True, blank=True)
   
    def __str__(self):
        return self.title
    
class Profile(models.Model):
    us = models.OneToOneField(User,on_delete=models.CASCADE)
    phone = models.IntegerField()
    email =models.CharField(max_length=30)
    address=models.CharField(max_length=200,null=True,blank=True)

    def __str__(self):
        return str(self.us)


class Comment(models.Model):
    us = models.ForeignKey(User,on_delete=models.CASCADE)
    cmnt = models.TextField()
    post = models.ForeignKey(Product,on_delete=models.CASCADE)

    def __str__(self):
        return str(self.us)

# =============================================================
class Wishlist(models.Model):
    us = models.ForeignKey(User, on_delete=models.CASCADE)  
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('us', 'product')  

    def __str__(self):
        return f"{self.us.username} - {self.product.name}"  
    
# ==========================================
class Blog(models.Model):
    title = models.CharField(max_length=100)
    details = models.CharField(max_length=2000)

    def __str__(self):
        return self.title

# ============================================
class Cart(models.Model):
    us = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"


