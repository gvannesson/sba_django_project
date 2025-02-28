from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.core.validators import RegexValidator


class User(AbstractUser):
    company_name = models.CharField("Company Name", max_length=250, blank=True)
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',  # Allows optional "+" and 9-15 digits
        message="Phone number must be entered in the format: '+123456789' (9-15 digits)."
    )
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    STATES = [
    ('AL', 'Alabama'),
    ('AK', 'Alaska'),
    ('AZ', 'Arizona'),
    ('AR', 'Arkansas'),
    ('CA', 'California'),
    ('CO', 'Colorado'),
    ('CT', 'Connecticut'),
    ('DE', 'Delaware'),
    ('DC', 'District of Columbia'),
    ('FL', 'Florida'),
    ('GA', 'Georgia'),
    ('HI', 'Hawaii'),
    ('ID', 'Idaho'),
    ('IL', 'Illinois'),
    ('IN', 'Indiana'),
    ('IA', 'Iowa'),
    ('KS', 'Kansas'),
    ('KY', 'Kentucky'),
    ('LA', 'Louisiana'),
    ('ME', 'Maine'),
    ('MD', 'Maryland'),
    ('MA', 'Massachusetts'),
    ('MI', 'Michigan'),
    ('MN', 'Minnesota'),
    ('MS', 'Mississippi'),
    ('MO', 'Missouri'),
    ('MT', 'Montana'),
    ('NE', 'Nebraska'),
    ('NV', 'Nevada'),
    ('NH', 'New Hampshire'),
    ('NJ', 'New Jersey'),
    ('NM', 'New Mexico'),
    ('NY', 'New York'),
    ('NC', 'North Carolina'),
    ('ND', 'North Dakota'),
    ('OH', 'Ohio'),
    ('OK', 'Oklahoma'),
    ('OR', 'Oregon'),
    ('PA', 'Pennsylvania'),
    ('RI', 'Rhode Island'),
    ('SC', 'South Carolina'),
    ('SD', 'South Dakota'),
    ('TN', 'Tennessee'),
    ('TX', 'Texas'),
    ('UT', 'Utah'),
    ('VT', 'Vermont'),
    ('VA', 'Virginia'),
    ('WA', 'Washington'),
    ('WV', 'West Virginia'),
    ('WI', 'Wisconsin'),
    ('WY', 'Wyoming')
]

    state = models.CharField(max_length=2, choices = STATES, null=True, default='IN')
    NAICS = models.CharField(max_length=6, blank=True)
    URBAN_RURAL_CHOICES = [
        ('1', 'Urban'),
        ('0', 'Rural'),
    ]
    urbanrural = models.CharField(max_length=1, choices=URBAN_RURAL_CHOICES, null=True, default='n')
    franchisecode = models.PositiveIntegerField(max_length=50, null=True, default='0')
    role = models.IntegerField(null=True, default=0) # 0 = company , 1 = advisor
    no_emp = models.PositiveIntegerField(verbose_name="Number of employees", null=True, default=0)
    username = models.CharField(max_length=100,blank=True)
    USERNAME_FIELD = "email"
    email = models.EmailField(('email address'), unique=True) # changes email to unique and blank to false
    REQUIRED_FIELDS = []

    
class LoanRequest(models.Model):
    user_id = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    bank_loan = models.IntegerField(null=True, default=0)
    request_date = models.DateField(auto_now_add=True)
    LOW_DOC_CHOICES = [
        (True, 'Yes'),
        (False, 'No'),
    ]
    lowdoc = models.CharField(max_length=1, choices=LOW_DOC_CHOICES, null=True, default='n')
    sba_loan = models.IntegerField(null=True, default=0)
    revlinecr = models.CharField(max_length=50, null=True, default='0')
    term = models.IntegerField(null=True, default=0)
    reason = models.CharField(max_length=500, null=True, default='')
    status = models.IntegerField(null=True, default=0)
    prediction_result = models.CharField(max_length=500, null=True, default='Not predicted')


class News(models.Model):
    user_id = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    topic = models.CharField(max_length=250, blank=True)
    date_news = models.DateTimeField(null=True)
    content = models.TextField()
    publication_date = models.DateTimeField(default=timezone.now)
    news_url = models.URLField(max_length=200)


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
