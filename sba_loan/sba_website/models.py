from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.core.validators import RegexValidator


class User(AbstractUser):
    """
    Modèle représentant une entreprise avec divers attributs, y compris les informations de contact, 
    la localisation et les détails des employés.

    Attributs :
        company_name (str) : Le nom de l'entreprise.
        phone_number (str) : Le numéro de téléphone de l'entreprise, validé par une expression régulière.
        STATES (list) : Liste des choix représentant les états des États-Unis.
        state (str) : L'état dans lequel se trouve l'entreprise, représenté par un code d'état à 2 lettres.
        NAICS (str) : Le code NAICS (Système de classification des industries de l'Amérique du Nord) de l'entreprise.
        URBAN_RURAL_CHOICES (list) : Liste des choix pour distinguer entre zones urbaines et rurales.
        urbanrural (str) : Indique si l'entreprise se situe dans une zone urbaine ou rurale.
        franchisecode (int) : Un code de franchise unique attribué à l'entreprise.
        role (int) : Le rôle de l'utilisateur associé à l'entreprise (0 pour entreprise, 1 pour conseiller).
        no_emp (int) : Le nombre d'employés travaillant dans l'entreprise.
        username (str) : Le nom d'utilisateur de l'utilisateur associé à l'entreprise.
        email (str) : L'adresse email de l'utilisateur, qui doit être unique.
    """
    
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
    franchisecode = models.PositiveIntegerField(null=True, default='0')
    role = models.IntegerField(null=True, default=0) # 0 = company , 1 = advisor
    no_emp = models.PositiveIntegerField(verbose_name="Number of employees", null=True, default=0)
    username = models.CharField(max_length=100,blank=True)
    USERNAME_FIELD = "email"
    email = models.EmailField(('email address'), unique=True) # changes email to unique and blank to false
    REQUIRED_FIELDS = []

    
class LoanRequest(models.Model):
    """
    Modèle représentant une demande de prêt d'un utilisateur avec diverses informations sur la demande.

    Attributs :
        user_id (ForeignKey) : Clé étrangère pointant vers l'utilisateur qui fait la demande de prêt.
        bank_loan (int) : Montant du prêt bancaire demandé.
        request_date (date) : Date de la demande de prêt, définie automatiquement à la date de création.
        LOW_DOC_CHOICES (list) : Liste des choix pour indiquer si la demande est un prêt à faible documentation.
        lowdoc (str) : Indique si la demande de prêt est à faible documentation (Oui ou Non).
        sba_loan (int) : Montant du prêt SBA (Small Business Administration) demandé.
        revlinecr (str) : Ligne de crédit disponible pour l'entreprise, sous forme de chaîne de caractères.
        term (int) : Durée du prêt en mois.
        reason (str) : Raison de la demande de prêt, sous forme de texte libre.
        status (int) : Statut de la demande de prêt (par exemple, en attente, approuvée, rejetée).
        prediction_result (str) : Résultat de la prédiction associée à la demande de prêt (par défaut "Non prédite").
    """

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
    """
    Modèle représentant une actualité publiée par un utilisateur.

    Attributs :
        user_id (ForeignKey) : Clé étrangère pointant vers l'utilisateur qui a publié l'actualité.
        title (str) : Le titre de l'actualité.
        topic (str) : Le sujet ou la catégorie de l'actualité.
        date_news (datetime) : La date et l'heure de l'événement lié à l'actualité.
        content (str) : Le contenu détaillé de l'actualité.
        publication_date (datetime) : La date et l'heure de la publication de l'actualité, définie par défaut à la date actuelle.
        news_url (str) : L'URL de l'actualité pour redirection vers la source originale.
    """

    user_id = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    title = models.CharField(max_length=250, blank=True)
    topic = models.CharField(max_length=250, blank=True)
    date_news = models.DateTimeField(null=True)
    content = models.TextField()
    publication_date = models.DateTimeField(default=timezone.now)
    news_url = models.URLField(max_length=200)