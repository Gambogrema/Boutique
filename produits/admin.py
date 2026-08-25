from django.contrib import admin
from .models import Produit


@admin.register(Produit)
class ProduitAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prix', 'stock', 'date_ajout')
    search_fields = ('nom', 'description')
    list_filter = ('date_ajout',)
