from django.db import models
from django.contrib.auth.models import User


class Fournisseur(models.Model):
    nom = models.CharField(max_length=200)
    pays = models.CharField(max_length=100)
    telephone = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True)
    adresse = models.TextField(blank=True)
    site_web = models.URLField(blank=True)
    actif = models.BooleanField(default=True)

    utilisateur = models.OneToOneField(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="fournisseur",
    )

    date_ajout = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nom
