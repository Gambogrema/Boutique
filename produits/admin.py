from django.contrib import admin

from .models import Produit, ProduitFournisseur


class ProduitFournisseurInline(admin.TabularInline):
    model = ProduitFournisseur
    extra = 1

    fields = (
        "fournisseur",
        "prix_fournisseur",
        "stock_fournisseur",
        "reference_fournisseur",
        "url_produit",
        "actif",
    )


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
        "fournisseurs__fournisseur__nom",
        "fournisseurs__reference_fournisseur",
    )

    list_filter = (
        "fournisseur",
        "date_ajout",
    )

    inlines = [
        ProduitFournisseurInline,
    ]

    @admin.display(description="💰 Marge")
    def afficher_marge(self, obj):
        marge = obj.prix - obj.prix_fournisseur
        return f"{marge} FCFA"


@admin.register(ProduitFournisseur)
class ProduitFournisseurAdmin(admin.ModelAdmin):
    list_display = (
        "produit",
        "fournisseur",
        "prix_fournisseur",
        "stock_fournisseur",
        "reference_fournisseur",
        "actif",
        "date_ajout",
    )

    list_filter = (
        "fournisseur",
        "actif",
        "date_ajout",
    )

    search_fields = (
        "produit__nom",
        "fournisseur__nom",
        "reference_fournisseur",
    )

    list_editable = (
        "prix_fournisseur",
        "stock_fournisseur",
        "actif",
    )

    ordering = (
        "produit__nom",
        "fournisseur__nom",
    )
