from django.contrib import admin

from .models import Produit


@admin.register(Produit)
class ProduitAdmin(admin.ModelAdmin):
    list_display = (
        "nom",
        "fournisseur",
        "prix_fournisseur",
        "prix",
        "afficher_marge",
        "stock",
        "date_ajout",
    )

    search_fields = (
        "nom",
        "description",
        "fournisseur__nom",
    )

    list_filter = (
        "fournisseur",
        "date_ajout",
    )

    @admin.display(description="💰 Marge")
    def afficher_marge(self, obj):
        marge = obj.prix - obj.prix_fournisseur
        return f"{marge} FCFA"
