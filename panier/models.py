from django.db import models
from fournisseurs.models import Fournisseur


class Commande(models.Model):
    nom = models.CharField(max_length=200)
    telephone = models.CharField(max_length=30)
    adresse = models.TextField()
    total = models.DecimalField(max_digits=10, decimal_places=2)

    MOYEN_PAIEMENT_CHOIX = [
        ("mtn", "MTN Mobile Money"),
        ("orange", "Orange Money"),
    ]

    STATUT_PAIEMENT_CHOIX = [
        ("en_attente", "En attente"),
        ("reussi", "Réussi"),
        ("echoue", "Échoué"),
    ]

    moyen_paiement = models.CharField(
        max_length=20,
        choices=MOYEN_PAIEMENT_CHOIX,
        default="mtn",
    )

    statut_paiement = models.CharField(
        max_length=20,
        choices=STATUT_PAIEMENT_CHOIX,
        default="en_attente",
    )

    STATUT_CHOIX = [
        ("en_attente", "En attente"),
        ("confirmee", "Confirmée"),
        ("envoyee_fournisseur",
     "Envoyée au fournisseur"),
        ("livraison", "En livraison"),
        ("livree", "Livrée"),
        ("annulee", "Annulée"),
    ]
    statut = models.CharField(
        max_length=20,
        choices=STATUT_CHOIX,
        default="en_attente",
    )

    date_commande = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Commande de {self.nom} - {self.total} FCFA"


class LigneCommande(models.Model):
    commande = models.ForeignKey(
        Commande,
        on_delete=models.CASCADE,
        related_name="lignes",
    )

    produit = models.ForeignKey(
        "produits.Produit",
        on_delete=models.PROTECT,
        related_name="lignes_commande",
    )

    fournisseur = models.ForeignKey(
        Fournisseur,
        on_delete=models.PROTECT,
        related_name="lignes_commande",
    )

    quantite = models.PositiveIntegerField()

    prix_vente = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    prix_fournisseur = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    def sous_total(self):
        return self.prix_vente * self.quantite

    def marge(self):
        return (
            self.prix_vente - self.prix_fournisseur
        ) * self.quantite

    def __str__(self):
        return (
            f"{self.quantite} x {self.produit.nom} "
            f"(Commande #{self.commande.id})"
        )
