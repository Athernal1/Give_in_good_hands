from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=64)


class Institution(models.Model):
    FOUNDATION = 'F'
    NON_GOVERNMENTAL = 'NG'
    LOCAL_COLLECTION = 'LC'

    TYPE_CHOICES = [
        (FOUNDATION, 'Foundation'),
        (NON_GOVERNMENTAL, 'Non-governmental'),
        (LOCAL_COLLECTION, 'Local collection'),
    ]

    name = models.CharField(max_length=64)
    description = models.TextField()
    type_of_institution = models.CharField(max_length=2, choices=TYPE_CHOICES, default=FOUNDATION)
    categories = models.ManyToManyField(Category)


class Donation(models.Model):
    quantity = models.IntegerField()
    categories = models.ManyToManyField(Category)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    address = models.CharField(max_length=128)
    phone_number = models.IntegerField()
    city = models.CharField(max_length=64)
    zip_code = models.CharField(max_length=16)
    pick_up_date = models.DateField()
    pick_up_time = models.TimeField()
    pick_up_comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, default=None)


