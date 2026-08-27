from django.shortcuts import render
from .models import Produit


def accueil(request):
    produits = Produit.objects.all()

    panier = request.session.get("panier", {})
    nombre_articles = sum(panier.values())

    return render(request, "produits/accueil.html", {
        "produits": produits,
        "nombre_articles": nombre_articles,
    })
