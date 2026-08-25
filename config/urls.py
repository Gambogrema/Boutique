from django.contrib import admin
from django.urls import path
from produits.views import accueil

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", accueil, name="accueil"),
]
