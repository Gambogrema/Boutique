from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

def connexion_fournisseur(request):
    erreur = None

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")

        utilisateur = authenticate(
            request,
            username=username,
            password=password,
        )

        if utilisateur is not None:
            if hasattr(utilisateur, "fournisseur") and utilisateur.fournisseur.actif:
                login(request, utilisateur)
                return redirect("tableau_de_bord_fournisseur")

            erreur = "Ce compte n'est pas associé à un fournisseur actif."
        else:
            erreur = "Nom d'utilisateur ou mot de passe incorrect."

    return render(
        request,
        "fournisseurs/connexion.html",
        {
            "erreur": erreur,
        },
    )


@login_required
def deconnexion_fournisseur(request):
    logout(request)
    return redirect("connexion_fournisseur")


@login_required
def tableau_de_bord_fournisseur(request):
    fournisseur = request.user.fournisseur

    from panier.models import LigneCommande

    lignes = (
        LigneCommande.objects
        .filter(fournisseur=fournisseur)
        .select_related("commande", "produit")
        .order_by("-commande__date_commande")
    )

    total_commandes = lignes.values("commande").distinct().count()

    montant_a_recevoir = sum(
        (ligne.prix_fournisseur * ligne.quantite for ligne in lignes),
        0,
    )

    chiffre_affaires = sum(
        (ligne.prix_vente * ligne.quantite for ligne in lignes),
        0,
    )

    marge_totale = sum(
        (ligne.marge() for ligne in lignes),
        0,
    )

    return render(
        request,
        "fournisseurs/tableau_de_bord.html",
        {
            "fournisseur": fournisseur,
            "lignes": lignes,
            "total_commandes": total_commandes,
            "montant_a_recevoir": montant_a_recevoir,
            "chiffre_affaires": chiffre_affaires,
            "marge_totale": marge_totale,
        },
    )
@login_required
def changer_statut_commande(request, ligne_id):
    from panier.models import LigneCommande

    if request.method != "POST":
        return redirect("tableau_de_bord_fournisseur")

    fournisseur = request.user.fournisseur

    ligne = get_object_or_404(
        LigneCommande,
        id=ligne_id,
        fournisseur=fournisseur,
    )

    nouveau_statut = request.POST.get("statut")

    statuts_autorises = [
        "envoyee_fournisseur",
        "livraison",
        "livree",
    ]

    if nouveau_statut in statuts_autorises:
        ligne.commande.statut = nouveau_statut
        ligne.commande.save(update_fields=["statut"])

    return redirect("tableau_de_bord_fournisseur")
