from django.contrib import admin
from .models import Commande, LigneCommande


@admin.action(description="📦 Marquer les commandes comme livrées")
def marquer_livrees(modeladmin, request, queryset):
    queryset.update(statut="livree")


@admin.action(description="🚚 Marquer les commandes en livraison")
def marquer_livraison(modeladmin, request, queryset):
    queryset.update(statut="livraison")


@admin.action(description="✅ Confirmer les commandes")
def confirmer_commandes(modeladmin, request, queryset):
    queryset.update(statut="confirmee")
@admin.action(description="📤 Envoyer les commandes au fournisseur")
def envoyer_aux_fournisseurs(modeladmin, request, queryset):
    queryset.update(statut="envoyee_fournisseur")

@admin.action(description="❌ Annuler les commandes")
def annuler_commandes(modeladmin, request, queryset):
    queryset.update(statut="annulee")


class LigneCommandeInline(admin.TabularInline):
    model = LigneCommande
    extra = 0

    readonly_fields = (
        "produit",
        "fournisseur",
        "quantite",
        "prix_vente",
        "prix_fournisseur",
        "afficher_marge",
    )

    fields = (
        "produit",
        "fournisseur",
        "quantite",
        "prix_vente",
        "prix_fournisseur",
        "afficher_marge",
    )

    @admin.display(description="💰 Marge")
    def afficher_marge(self, obj):
        return f"{obj.marge()} FCFA"


@admin.register(Commande)
class CommandeAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "nom",
        "telephone",
        "total",
        "afficher_marge_totale",
        "afficher_moyen_paiement",
        "afficher_statut_paiement",
        "statut",
        "date_commande",
    )

    list_filter = (
        "moyen_paiement",
        "statut_paiement",
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
envoyer_aux_fournisseurs,
marquer_livraison,
        marquer_livrees,
        annuler_commandes,
    )

    inlines = [LigneCommandeInline]

    @admin.display(description="📈 Marge totale")
    def afficher_marge_totale(self, obj):
        return f"{sum((ligne.marge() for ligne in obj.lignes.all()), 0)} FCFA"

    @admin.display(description="💳 Moyen de paiement")
    def afficher_moyen_paiement(self, obj):

        if obj.moyen_paiement == "mtn":
            return "🟡 MTN Mobile Money"

        if obj.moyen_paiement == "orange":
            return "🟠 Orange Money"

        return "❓ Non défini"

    @admin.display(description="💰 Statut paiement")
    def afficher_statut_paiement(self, obj):

        if obj.statut_paiement == "en_attente":
            return "🕐 En attente"

        if obj.statut_paiement == "reussi":
            return "✅ Réussi"

        if obj.statut_paiement == "echoue":
            return "❌ Échoué"

        return "❓ Inconnu"


@admin.register(LigneCommande)
class LigneCommandeAdmin(admin.ModelAdmin):

    list_display = (
        "commande",
        "produit",
        "fournisseur",
        "quantite",
        "prix_vente",
        "prix_fournisseur",
        "afficher_marge",
    )

    list_filter = (
        "produit",
        "fournisseur",
    )

    search_fields = (
        "commande__nom",
        "produit__nom",
        "fournisseur__nom",
    )

    @admin.display(description="💰 Marge")
    def afficher_marge(self, obj):
        return f"{obj.marge()} FCFA"
