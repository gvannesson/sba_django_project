from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    company_name = models.CharField("Name", max_length=250, blank=True)
    phone_number = models.CharField(max_length=10, blank=True)
    state = models.CharField(max_length=100, blank=True)
    NAICS = models.CharField(max_length=100, blank=True)
    URBAN_RURAL_CHOICES = [
        ('y', 'Urban'),
        ('n', 'Rural'),
    ]
    urbanrural = models.CharField(max_length=1, choices=URBAN_RURAL_CHOICES, null=True, default='n')
    franchisecode = models.CharField(max_length=50, null=True, default='0')
    role = models.IntegerField(null=True, default=0) # 0 = company , 1 = advisor
    USERNAME_FIELD = "email"


class LoanRequest(models.Model):
    user_id = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    bank_loan = models.IntegerField(null=True, default=0)
    request_date = models.DateField(auto_now_add=True)
    LOW_DOC_CHOICES = [
        ('y', 'Yes'),
        ('n', 'No'),
    ]
    lowdoc = models.CharField(max_length=1, choices=LOW_DOC_CHOICES, null=True, default='n')
    sba_loan = models.IntegerField(null=True, default=0)
    revlinecr = models.CharField(max_length=50, null=True, default='0')
    term = models.IntegerField(null=True, default=0)
    reason = models.CharField(max_length=500, null=True, default='')


class News(models.Model):
    user_id = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    items = models.CharField("Name", max_length=250, blank=True)
    date_news = models.DateTimeField(auto_now_add=True)
    news_url = models.URLField(max_length=200)

    def __str__(self):
        return self.news_url  # Retourne l'URL des actualités



'''
class User(AbstractUser):

    email sert d'identifiant
    name = models.CharField("Name", max_length=250, blank=True)
    Numéro de téléphone
    state = models.CharField(max_length=100, blank=True)
    NAICS = models.CharField(max_length=100, blank=True)
    URBAN_RURAL_CHOICES = [
        ('y', 'Urban'),
        ('n', 'Rural'),
    ]
    urbanrural = models.CharField(max_length=1, choices=URBAN_RURAL_CHOICES, null=True, default='n')
    franchisecode = models.CharField(max_length=50, null=True, default='0')
    role = models.IntegerField(null=True, default=0) # 0 = company , 1 = advisor


UPDATE -->> email, numéro de téléphone, password



    LoanRequest

    Rempli par le demandeur
            user_id (automatique)
            bank_loan
            request_date (automatique date.now)
            raison du prêt

    Rempli par l'advisor
            LOW_DOC_CHOICES = [
                ('y', 'Yes'),
                ('n', 'No'),
            ]
            lowdoc = models.CharField(max_length=1, choices=LOW_DOC_CHOICES, null=True, default='n')
            sba_loan = models.IntegerField(null=True, default=0)
            revlinecr = models.CharField(max_length=50, null=True, default='0')
            term = models.IntegerField(null=True, default=0)

    Rempli par l'API
            status ("en attente", "décliné", "acceptée")



    News
            date
            topic



'''