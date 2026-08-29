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
    date_ajout = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nom
