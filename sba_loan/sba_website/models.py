from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    name = models.CharField("Name", max_length=250, blank=True)
    state = models.CharField(max_length=100, blank=True)
    NAICS = models.CharField(max_length=100, blank=True)
    
    # Choix pour urbanrural et lowdoc
    URBAN_RURAL_CHOICES = [
        ('y', 'Urban'),
        ('n', 'Rural'),
    ]
    urbanrural = models.CharField(max_length=1, choices=URBAN_RURAL_CHOICES, null=True, default='n')

    LOW_DOC_CHOICES = [
        ('y', 'Yes'),
        ('n', 'No'),
    ]
    lowdoc = models.CharField(max_length=1, choices=LOW_DOC_CHOICES, null=True, default='n')

    bank_loan = models.IntegerField(null=True, default=0)
    sba_loan = models.IntegerField(null=True, default=0)
    franchisecode = models.CharField(max_length=50, null=True, default='0')
    revlinecr = models.CharField(max_length=50, null=True, default='0')
    term = models.IntegerField(null=True, default=0)
    role = models.IntegerField(null=True, default=0) # 0 = company, 1=advisor


