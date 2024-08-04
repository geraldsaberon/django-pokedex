from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = "pokedex"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("<int:pk>/", views.PokemonView.as_view(), name="pokemon-detail"),
    path("<int:pk>/edit/", views.PokemonEditView.as_view(), name="pokemon-edit"),
    path("<int:pk>/delete/", views.PokemonDeleteView.as_view(), name="pokemon-delete"),
    path("create/", views.PokemonCreateView.as_view(), name="pokemon-create"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("register/", views.RegisterView.as_view(), name="register"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
