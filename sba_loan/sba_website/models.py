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
    role = models.IntegerField(null=True, default=0) # 0 = company , 1 = advisor

class LoanRequests(models.Model):
    name_company = models.CharField(max_length=150, null=True)
    loan_amount = models.FloatField(default=0)
    date_requests = models.DateField(auto_now=False, auto_now_add=True)

class Message(models.Model):
    username_sender = models.CharField("Name", max_length=250, blank=True)
    username_receiver = models.CharField("Name", max_length=250, blank=True)
    date_message = models.DateField(auto_now=False, auto_now_add=True)

class News(models.Model):
    items = models.CharField("Name", max_length=250, blank=True)
    date_news = models.DateTimeField(null=True)
    news_url = models.URLField(max_length=200)

    def __str__(self):
        return self.news_url  # Retourne l'URL des actualités
