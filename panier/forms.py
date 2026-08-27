from django import forms
from .models import Commande


class CommandeForm(forms.ModelForm):
    class Meta:
        model = Commande
        fields = ["nom", "telephone", "adresse"]

        widgets = {
            "nom": forms.TextInput(attrs={
                "placeholder": "Votre nom",
            }),
            "telephone": forms.TextInput(attrs={
                "placeholder": "Votre numéro de téléphone",
            }),
            "adresse": forms.Textarea(attrs={
                "placeholder": "Votre adresse",
                "rows": 4,
            }),
        }
