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
            "produit_id": produit.id,
            "quantite": quantite,
            "sous_total": sous_total,
        })

        total += sous_total

    return render(request, "panier/panier.html", {
        "produits": produits,
        "total": total,
    })


def augmenter_quantite(request, produit_id):
    panier = request.session.get("panier", {})
    produit_id = str(produit_id)

    if produit_id in panier:
        panier[produit_id] += 1

    request.session["panier"] = panier
    request.session.modified = True

    return redirect("panier")


def diminuer_quantite(request, produit_id):
    panier = request.session.get("panier", {})
    produit_id = str(produit_id)

    if produit_id in panier:
        panier[produit_id] -= 1

        if panier[produit_id] <= 0:
            del panier[produit_id]

    request.session["panier"] = panier
    request.session.modified = True

    return redirect("panier")
def supprimer_du_panier(request, produit_id):
    panier = request.session.get("panier", {})
    produit_id = str(produit_id)

    if produit_id in panier:
        del panier[produit_id]

    request.session["panier"] = panier
    request.session.modified = True

    return redirect("panier")
