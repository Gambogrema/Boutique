from django.shortcuts import redirect, get_object_or_404, render
from produits.models import Produit


def ajouter_au_panier(request, produit_id):
    produit = get_object_or_404(Produit, id=produit_id)

    panier = request.session.get("panier", {})
    produit_id = str(produit_id)

    if produit_id in panier:
        panier[produit_id] += 1
    else:
        panier[produit_id] = 1

    request.session["panier"] = panier
    request.session.modified = True

    return redirect("accueil")


def afficher_panier(request):
    panier = request.session.get("panier", {})

    produits = []
    total = 0

    for produit_id, quantite in panier.items():
        produit = get_object_or_404(Produit, id=produit_id)
        sous_total = produit.prix * quantite

        produits.append({
            "produit": produit,
            "quantite": quantite,
            "sous_total": sous_total,
        })

        total += sous_total

    return render(request, "panier/panier.html", {
        "produits": produits,
        "total": total,
    })
