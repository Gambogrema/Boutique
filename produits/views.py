from django.shortcuts import render
from .models import Produit


def accueil(request):
    produits = Produit.objects.all()
    return render(request, "produits/accueil.html", {
        "produits": produits
    })
