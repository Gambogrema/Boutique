from django.contrib import admin
from django.urls import include, path
from produits.views import accueil

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", accueil, name="accueil"),
    path("panier/", include("panier.urls")),
]
