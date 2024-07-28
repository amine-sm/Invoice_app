from django.contrib import admin
from .models import *
from django.utils.translation import gettext_lazy as _ 

# Register your models here.
class AdminArticle(admin.ModelAdmin):
    list_display = ('facture', 'name', 'quantite', 'code_bar', 'prix_unite', 'total')

class AdminCustomer(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'address', 'sex', 'age', 'city', 'zip_code', 'created_date', 'saved_by')

class AdminFacture(admin.ModelAdmin):
    list_display = ('customer', 'saved_by', 'facture_date', 'total', 'last_updated_date', 'paid', 'facture_type', 'commenter')

admin.site.register(Article, AdminArticle)
admin.site.register(Customer, AdminCustomer)
admin.site.register(Facture, AdminFacture)

# Définir les titres personnalisés comme des chaînes de caractères directement
admin.site.site_title = "Facturation System"
admin.site.index_title = "Facturation System"
admin.site.site_header = "Facturation System"
