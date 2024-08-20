from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.TextField()
    msg = models.TextField(null=True, blank=True, default=None)
    city = models.CharField(max_length=100)
    
    def _str_(self):
        return self.city

class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    stock = models.IntegerField()
    title = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    discount = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, default=0.00)  # Percentage discount
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()

    def __str__(self):
        return self.title

    def get_discounted_price(self):
        if self.discount:
            return self.price * (1 - (self.discount / 100))
        return self.price

class Colour(models.Model):
    colour_id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    colour = models.CharField(max_length=30)

    def __str__(self):
        return self.colour


class Image(models.Model):
    image_id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='product_images/')


    def __str__(self):
        return f"Image for {self.product.title}"

class Size(models.Model):
    size_id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.CharField(max_length=30)

    def __str__(self):
        return self.size



class Cart(models.Model):
    cart_id = models.AutoField(primary_key=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=False, default=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, default=1)  # Assuming user ID 1 exists

    def __str__(self):
        return f"Cart ID: {self.cart_id}"

class CartItem(models.Model):
    cart_item_id = models.AutoField(primary_key=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='items')
    quantity = models.PositiveIntegerField(default=1)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    colour = models.ForeignKey(Colour, on_delete=models.CASCADE)


    def __str__(self):
        return f"CartItem ID: {self.cart_item_id}, Product: {self.product.title}, Quantity: {self.quantity}"

    def get_total_price(self):
        discounted_price = self.product.get_discounted_price()
        return discounted_price * self.quantity



class Supplier(models.Model):
    supplier_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    # ISS PR MAXIMUM 12 DECIMALS KI RESTRICTIONS LAGANI HAI THROUGH FORMS AUR VIEWS
    contact_number =models.IntegerField()

    def __str__(self):
        return f"Supplier ID: {self.supplier_id}, Name: {self.name}, Contact Number: {self.contact_number}"


class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    delivery_status = models.CharField(max_length=100)
    order_date = models.DateField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    status_last_updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Order ID: {self.order_id}, Status: {self.delivery_status}, Date: {self.order_date}, Amount: {self.total_amount}"


