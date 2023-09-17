from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

class Company(models.Model):
    name = models.CharField(max_length=255)
    stock_price = models.DecimalField(max_digits=10, decimal_places=2)
    high_52week = models.DecimalField(max_digits=10, decimal_places=2)
    low_52week = models.DecimalField(max_digits=10, decimal_places=2)
    profit_margin = models.DecimalField(max_digits=5, decimal_places=2)
    volume = models.IntegerField()
    pe_ratio = models.DecimalField(max_digits=5, decimal_places=2)

    def str(self):
        return self.name


