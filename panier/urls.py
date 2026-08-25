from django.urls import path
from .views import ajouter_au_panier, afficher_panier

urlpatterns = [
    path("", afficher_panier, name="panier"),
    path("ajouter/<int:produit_id>/", ajouter_au_panier, name="ajouter_au_panier"),
]
