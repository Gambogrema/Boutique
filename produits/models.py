from django.db import models

from fournisseurs.models import Fournisseur


class Produit(models.Model):
    nom = models.CharField(max_length=200)

    description = models.TextField()

    prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    prix_fournisseur = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
    )

    fournisseur = models.ForeignKey(
        Fournisseur,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="produits",
    )

    stock = models.PositiveIntegerField(default=0)

    image = models.ImageField(
        upload_to="produits/",
        blank=True,
        null=True,
    )

    date_ajout = models.DateTimeField(
        auto_now_add=True,
    )

    def meilleur_fournisseur(self, quantite=1):
        return (
            self.fournisseurs
            .filter(
                actif=True,
                stock_fournisseur__gte=quantite,
            )
            .order_by("prix_fournisseur")
            .first()
        )

    def __str__(self):
        return self.nom


class ProduitFournisseur(models.Model):
    produit = models.ForeignKey(
        Produit,
        on_delete=models.CASCADE,
        related_name="fournisseurs",
    )

    fournisseur = models.ForeignKey(
        Fournisseur,
        on_delete=models.PROTECT,
        related_name="produits_fournisseur",
    )

    prix_fournisseur = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    stock_fournisseur = models.PositiveIntegerField(
        default=0,
    )

    reference_fournisseur = models.CharField(
        max_length=200,
        blank=True,
    )

    url_produit = models.URLField(
        blank=True,
    )

    actif = models.BooleanField(
        default=True,
    )

    date_ajout = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["produit", "fournisseur"],
                name="unique_produit_fournisseur",
            )
        ]

    def __str__(self):
        return f"{self.produit.nom} - {self.fournisseur.nom}"
