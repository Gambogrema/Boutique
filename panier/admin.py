from django.contrib import admin
from .models import Commande


@admin.action(description="📦 Marquer les commandes comme livrées")
def marquer_livrees(modeladmin, request, queryset):
    queryset.update(statut="livree")


@admin.action(description="🚚 Marquer les commandes en livraison")
def marquer_livraison(modeladmin, request, queryset):
    queryset.update(statut="livraison")


@admin.action(description="✅ Confirmer les commandes")
def confirmer_commandes(modeladmin, request, queryset):
    queryset.update(statut="confirmee")


@admin.action(description="❌ Annuler les commandes")
def annuler_commandes(modeladmin, request, queryset):
    queryset.update(statut="annulee")


@admin.register(Commande)
class CommandeAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "nom",
        "telephone",
        "total",
        "statut",
        "date_commande",
    )

    list_filter = (
        "statut",
        "date_commande",
    )

    search_fields = (
        "nom",
        "telephone",
        "adresse",
    )

    list_editable = (
        "statut",
    )

    ordering = (
        "-date_commande",
    )

    actions = (
        confirmer_commandes,
        marquer_livraison,
        marquer_livrees,
        annuler_commandes,
    )
