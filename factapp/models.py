from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
    SEX_TYPES = [
        ('M', 'masculin'),
        ('F', 'feminin'),
    ]
    
    name = models.CharField(max_length=132)
    email = models.EmailField()
    phone = models.CharField(max_length=132)
    address = models.CharField(max_length=132)
    sex = models.CharField(max_length=1, choices=SEX_TYPES)
    age = models.CharField(max_length=12)
    city = models.CharField(max_length=32)
    zip_code = models.CharField(max_length=16)
    created_date = models.DateTimeField(auto_now_add=True)
    saved_by = models.ForeignKey(User, on_delete=models.PROTECT)

    class Meta:
        verbose_name = "Customer"
        verbose_name_plural = "Customers"

    def __str__(self):
        return self.name

class Facture(models.Model):
    FACTURE_TYPES = [
        ('R', 'RECU'),
        ('P', 'PROFOMAT'),
        ('F', 'FACTURE'),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    saved_by = models.ForeignKey(User, on_delete=models.PROTECT)
    facture_date = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    last_updated_date = models.DateTimeField(null=True, blank=True)
    paid = models.BooleanField(default=False)
    facture_type = models.CharField(max_length=1, choices=FACTURE_TYPES)
    commenter = models.TextField(max_length=1000, null=True, blank=True)

    class Meta:
        verbose_name = "Facture"
        verbose_name_plural = "Factures"

    def __str__(self):
        return f"Facture {self.facture_date} - {self.customer.name}"

    @property 
    def get_total(self):
        articles = self.article_set.all()
        total = sum(article.get_total for article in articles)
        return total

class Article(models.Model):
    facture = models.ForeignKey(Facture, on_delete=models.CASCADE)
    name = models.CharField(max_length=32)
    quantite = models.IntegerField()
    code_bar = models.CharField(max_length=320, default='')  
    prix_unite = models.DecimalField(max_digits=10000, decimal_places=2)
    total = models.DecimalField(max_digits=10000, decimal_places=2)
    
    class Meta:
        verbose_name = "Article"
        verbose_name_plural = "Articles"

    @property 
    def get_total(self):
        total = self.quantite * self.prix_unite
        return total
