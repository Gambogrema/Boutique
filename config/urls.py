from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from produits.views import accueil

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", accueil, name="accueil"),
    path("panier/", include("panier.urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
