from django.db import models
from django import forms
import datetime
import json
from django.contrib.auth.models import User, Permission
from django.core.validators import MaxValueValidator, MinValueValidator

class product(models.Model):
    product_name = models.CharField(max_length=500, default='')
    product_image = models.FileField()
    product_type = models.CharField(max_length=500, default='')
    small_description = models.CharField(max_length=340, default='')
    price = models.FloatField()
    base_quantity = models.IntegerField()
    synonyms = models.TextField(null=True, default=" ")
    def __str__(self):
        return str(self.product_name)+' - '+str(self.product_type)

class product_description(models.Model):
    product_id = models.ForeignKey(product, on_delete=models.CASCADE)
    description = models.TextField()

    def __str__(self):
        return str(self.product_id)
class addresses(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    district = models.CharField(max_length=20, default='')
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    house_no = models.CharField(max_length=10)
    street=models.CharField(max_length=50)
    area = models.CharField(max_length=50)
    pin = models.IntegerField(default=328001, validators = [MaxValueValidator(999999), MinValueValidator(100000)])
    def __str__(self):
        return str(self.user.username)+' - '+str(self.city)

class shopping_cart_items(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    product_id = models.ForeignKey(product, null=True, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    amount_to_pay = models.IntegerField(default=0)
    def __str__(self):
        return str(self.user)+' - '+str(self.product_id)+' - '+str(self.quantity)

class all_orders_table(models.Model):
    user_object = models.ForeignKey(User, on_delete=models.CASCADE)
    ordered_item = models.ForeignKey(product, on_delete=models.CASCADE)
    quantity = models.FloatField(default=0.0)
    paying_amount = models.IntegerField(default=0)
    order_date = models.DateField()
    order_delievered = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user_object)+' - '+str(self.ordered_item)+' - '+str(self.quantity)
