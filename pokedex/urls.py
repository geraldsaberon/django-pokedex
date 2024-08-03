from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = "pokedex"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("<int:pokemon_number>/", views.PokemonView.as_view(), name="pokemon-detail"),
    path("<int:pokemon_number>/edit/", views.PokemonEditView.as_view(), name="pokemon-edit"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
