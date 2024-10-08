from django.http import HttpRequest, HttpResponse
from django.urls import reverse
from django.views import View, generic
from django.contrib.auth import login, views as auth_views
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Permission, User
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
from rest_framework import viewsets

from pokedex.forms import PokemonEditForm
from pokedex.models import Pokemon, PokemonType
from pokedex.serializers import PokemonSerializer
from pokedex.utils import create_pokemon, update_pokemon

# Create your views here.
class LoginView(auth_views.LoginView):
    template_name = "pokedex/login.html"
    next_page = "/"
    redirect_authenticated_user = True

class LogoutView(auth_views.LogoutView):
    next_page = "/"

class RegisterView(View):
    template_name = "pokedex/register.html"
    form_class = UserCreationForm

    def get(self, request: HttpRequest):
        if request.user.is_authenticated:
            return redirect("/")
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request: HttpRequest):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                form.cleaned_data["username"],
                password=form.cleaned_data["password1"])
            user.user_permissions.set([
                Permission.objects.get(codename="add_pokemon"),
                Permission.objects.get(codename="view_pokemon"),
                Permission.objects.get(codename="change_pokemon"),
                Permission.objects.get(codename="delete_pokemon"),
            ])
            login(request, user)
            return redirect("pokedex:index")
        else:
            return render(request, self.template_name, {"form": form})

class IndexView(View):
    template_name = "pokedex/index.html"

    def get(self, request: HttpRequest):
        pokemon_type = request.GET.get("type")
        pokemons = Pokemon.objects.filter(is_deleted=False)
        if pokemon_type != "all" and pokemon_type != None:
            pokemons = pokemons.filter(types__name=pokemon_type)
        context = {
            "pokemons": pokemons,
            "types": PokemonType.objects.order_by("name")
        }
        return render(request, self.template_name, context)

class PokemonView(View):
    queryset = Pokemon.objects.filter(is_deleted=False)
    template_name = "pokedex/pokemon_details.html"

    def get(self, request, pk):
        pokemon = self.queryset.get(pk=pk)

        prev_pokemon = self.queryset.filter(pk=pk-1)
        prev_pokemon = prev_pokemon.first() if prev_pokemon.exists() else None
        next_pokemon = self.queryset.filter(pk=pk+1)
        next_pokemon = next_pokemon.first() if next_pokemon.exists() else None

        context = {
            "pokemon": pokemon,
            "prev_pokemon": prev_pokemon,
            "next_pokemon": next_pokemon
        }

        return render(request, self.template_name, context)

class PokemonEditView(View):
    template_name = "pokedex/pokemon_edit.html"
    form_class = PokemonEditForm

    @method_decorator(never_cache)
    def get(self, request, pk):
        pokemon = get_object_or_404(Pokemon, pk=pk)

        initial_form_data = {"name": pokemon.name,}
        for i, type_ in enumerate(pokemon.types.all()):
            initial_form_data[f"type{i+1}"] = type_.name
        for i, ability in enumerate(pokemon.abilities.all()):
            initial_form_data[f"ability{i+1}"] = ability.name
        for stat in pokemon.stats.all():
            initial_form_data[stat.name.replace("-", "_")] = stat.base_stat

        form = self.form_class(initial_form_data)

        return render(request, self.template_name, {"pokemon": pokemon, "form": form})

    def post(self, request: HttpRequest, pk):
        pokemon = get_object_or_404(Pokemon, pk=pk)

        if not request.user.is_authenticated:
            return render(request, self.template_name, {"pokemon": pokemon})

        if not request.user.has_perm("pokedex.change_pokemon"):
            return render(request, self.template_name, status=403)

        form = self.form_class(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get("name")

            if Pokemon.objects.filter(name=name).exists() and pokemon.name != name:
                form.add_error("name", f"{name} already exists. Pokemon name must be unique")
                return render(request, self.template_name, {"pokemon": pokemon, "form": form})

            pokemon = update_pokemon(pokemon, **form.cleaned_data)

            return redirect("pokedex:pokemon-detail", pk=pokemon.pk)
        else:
            return render(request, self.template_name, {"pokemon": pokemon, "form": form})

class PokemonCreateView(View):
    template_name = "pokedex/pokemon_create.html"
    form_class = PokemonEditForm

    @method_decorator(never_cache)
    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request: HttpRequest):
        form = self.form_class(request.POST)

        if not request.user.is_authenticated:
            return render(request, self.template_name)

        if not request.user.has_perm("pokedex.add_pokemon"):
            return render(request, self.template_name, status=403)

        if form.is_valid():
            name = form.cleaned_data.get("name")

            if Pokemon.objects.filter(name=name).exists():
                form.add_error("name", f"{name} already exists. Pokemon name must be unique")
                return render(request, self.template_name, {"form": form})

            pokemon = create_pokemon(**form.cleaned_data)

            return redirect("pokedex:pokemon-detail", pk=pokemon.pk)
        else:
            return render(request, self.template_name, {"form": form})

class PokemonDeleteView(View):
    def post(self, request: HttpRequest, pk):
        if not request.user.has_perm("pokedex.delete_pokemon"):
            return redirect(reverse("pokedex:pokemon-detail", args=[pk]))

        if not request.user.is_authenticated:
            return redirect("pokedex:login")
        pokemon = get_object_or_404(Pokemon, pk=pk)
        pokemon.is_deleted = True
        pokemon.save()
        return redirect("pokedex:index")


# Djano REST Framework
class PokemonsViewSet(viewsets.ModelViewSet):
    queryset = Pokemon.objects.filter(is_deleted=False)
    serializer_class = PokemonSerializer

    def perform_destroy(self, instance: Pokemon):
        instance.is_deleted = True
        instance.save()
