from django.contrib import admin
from .models import Fournisseur


@admin.register(Fournisseur)
class FournisseurAdmin(admin.ModelAdmin):
    list_display = (
        "nom",
        "pays",
        "telephone",
        "email",
        "actif",
        "date_ajout",
    )

    list_filter = (
        "pays",
        "actif",
        "date_ajout",
    )

    search_fields = (
        "nom",
        "pays",
        "telephone",
        "email",
    )

    list_editable = (
        "actif",
    )

    ordering = (
        "-date_ajout",
    )
