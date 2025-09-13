from django.db import models
 
 
class Item(models.Model):
    item_name = models.CharField(max_length=150)
    item_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.item_name) 

class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to='menu_images/', blank=True, null=True)

    def __str__(self):
        return self.name


class TodaysSpecial(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to="specials/", blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)  
    def __str__(self):
        return self.name

class HomepageBanner(models.Model):
    title = models.CharField(max_length=200, blank=True, null=True)
    background_image = models.ImageField(upload_to="banners/")

    def __str__(self):
        return self.title if self.title else "Homepage Banner"
