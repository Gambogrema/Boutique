
from django.db import transaction
from django.shortcuts import redirect, get_object_or_404, render

from produits.models import Produit
from .models import Commande, LigneCommande
from .forms import CommandeForm

def ajouter_au_panier(request, produit_id):
    produit = get_object_or_404(Produit, id=produit_id)

    panier = request.session.get("panier", {})
    produit_id = str(produit_id)

    quantite_actuelle = panier.get(produit_id, 0)

    if produit.stock <= 0:
        return redirect("accueil")

    if quantite_actuelle >= produit.stock:
        return redirect("accueil")

    panier[produit_id] = quantite_actuelle + 1

    request.session["panier"] = panier
    request.session.modified = True

    return redirect("accueil")


def afficher_panier(request):
    panier = request.session.get("panier", {})

    produits = []
    total = 0
    nombre_articles = 0

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
        nombre_articles += quantite

    return render(request, "panier/panier.html", {
        "produits": produits,
        "total": total,
        "nombre_articles": nombre_articles,
    })


def augmenter_quantite(request, produit_id):
    produit = get_object_or_404(Produit, id=produit_id)

    panier = request.session.get("panier", {})
    produit_id = str(produit_id)

    if produit_id in panier:
        quantite_actuelle = panier[produit_id]

        if quantite_actuelle < produit.stock:
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

def passer_commande(request):
    panier = request.session.get("panier", {})

    if not panier:
        return redirect("panier")

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

    if request.method == "POST":
        form = CommandeForm(request.POST)

        if form.is_valid():
            stock_insuffisant = False

            for produit_id, quantite in panier.items():
                produit = get_object_or_404(
                    Produit,
                    id=produit_id,
                )

                if quantite > produit.stock:
                    stock_insuffisant = True

                    form.add_error(
                        None,
                        f"Stock insuffisant pour {produit.nom}. "
                        f"Stock disponible : {produit.stock}."
                    )

            if not stock_insuffisant:
                with transaction.atomic():
                    commande = form.save(commit=False)
                    commande.total = total
                    commande.save()

                    for produit_id, quantite in panier.items():
                        produit = get_object_or_404(
                            Produit,
                            id=produit_id,
                        )

                        LigneCommande.objects.create(
                            commande=commande,
                            produit=produit,
                            fournisseur=produit.fournisseur,
                            quantite=quantite,
                            prix_vente=produit.prix,
                            prix_fournisseur=produit.prix_fournisseur,
                        )

                        produit.stock -= quantite
                        produit.save(
                            update_fields=["stock"]
                        )

                request.session["panier"] = {}
                request.session.modified = True

                return redirect(
                    "commande_confirmation",
                    commande_id=commande.id,
                )

    else:
        form = CommandeForm()

    return render(
        request,
        "panier/commande.html",
        {
            "form": form,
            "produits": produits,
            "total": total,
        },
    )
def commande_confirmation(request, commande_id):
    commande = get_object_or_404(Commande, id=commande_id)

    return render(
        request,
        "panier/confirmation.html",
        {
            "commande": commande,
        },
    )


def suivi_commande(request, commande_id):
    commande = get_object_or_404(Commande, id=commande_id)

    return render(
        request,
        "panier/suivi.html",
        {
            "commande": commande,
        },
    )

def paiement(request, commande_id):
    commande = get_object_or_404(Commande, id=commande_id)

    # Une commande déjà payée ne peut pas être payée une deuxième fois
    if commande.statut_paiement == "reussi":
        return redirect(
            "paiement_reussi",
            commande_id=commande.id,
        )

    if request.method == "POST":
        moyen_paiement = request.POST.get("moyen_paiement")
        telephone = request.POST.get("telephone", "").strip()

        print("=== PAIEMENT REÇU ===")
        print("Moyen :", moyen_paiement)
        print("Téléphone :", telephone)

        # Vérification du moyen de paiement
        if moyen_paiement not in ["mtn", "orange"]:
            return render(
                request,
                "panier/paiement.html",
                {
                    "commande": commande,
                    "erreur": "Veuillez choisir MTN Mobile Money ou Orange Money.",
                },
            )

        # Nettoyage du numéro
        telephone = telephone.replace(" ", "").replace("-", "")

        # Vérification simple du numéro camerounais
        if (
            not telephone.isdigit()
            or len(telephone) != 9
            or not telephone.startswith("6")
        ):
            return render(
                request,
                "panier/paiement.html",
                {
                    "commande": commande,
                    "erreur": "Veuillez saisir un numéro camerounais valide de 9 chiffres.",
                },
            )

        # Enregistrement du paiement simulé
        commande.moyen_paiement = moyen_paiement
        commande.telephone = telephone
        commande.statut_paiement = "reussi"
        commande.statut = "confirmee"
        commande.save()

        print("=== PAIEMENT ENREGISTRÉ ===")
        print("Commande :", commande.id)
        print("Statut paiement :", commande.statut_paiement)
        print("Statut commande :", commande.statut)

        return redirect(
            "paiement_reussi",
            commande_id=commande.id,
        )

    return render(
        request,
        "panier/paiement.html",
        {
            "commande": commande,
        },
    )


def paiement_reussi(request, commande_id):
    commande = get_object_or_404(Commande, id=commande_id)

    return render(
        request,
        "panier/paiement_reussi.html",
        {
            "commande": commande,
        },
    )
