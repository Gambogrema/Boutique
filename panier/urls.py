from django.urls import path

from .views import (
    ajouter_au_panier,
    afficher_panier,
    augmenter_quantite,
    diminuer_quantite,
    supprimer_du_panier,
)


urlpatterns = [
    path("", afficher_panier, name="panier"),
    path(
        "ajouter/<int:produit_id>/",
        ajouter_au_panier,
        name="ajouter_au_panier",
    ),
    path(
        "augmenter/<int:produit_id>/",
        augmenter_quantite,
        name="augmenter_quantite",
    ),
    path(
        "diminuer/<int:produit_id>/",
        diminuer_quantite,
        name="diminuer_quantite",
    ),
    path(
        "supprimer/<int:produit_id>/",
        supprimer_du_panier,
        name="supprimer_du_panier",
    ),
]
