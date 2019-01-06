from django.db import models
import datetime

SELECT_OPERATION = (
    ('Expenses',''), ('Profits',''))


class Category(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, default=None)
    category = models.CharField(max_length=100, blank=False)
    description = models.CharField(max_length=300)


class Transaction(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, default=None)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    operation = models.CharField(max_length=9, blank=False, choices=SELECT_OPERATION)
    sum = models.DecimalField(max_digits=7, decimal_places=2)
    date_operation = models.DateField(default=datetime.date.today, blank=False)
    description = models.CharField(max_length=300)
# Create your models here.
