from django.urls import path
from . import views


urlpatterns = [
    path(
        "connexion/",
        views.connexion_fournisseur,
        name="connexion_fournisseur",
    ),

    path(
        "deconnexion/",
        views.deconnexion_fournisseur,
        name="deconnexion_fournisseur",
    ),

    path(
        "tableau-de-bord/",
        views.tableau_de_bord_fournisseur,
        name="tableau_de_bord_fournisseur",
    ),

    path(
        "commande/<int:ligne_id>/statut/",
        views.changer_statut_commande,
        name="changer_statut_commande",
    ),
]
