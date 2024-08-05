from django.http import HttpRequest, HttpResponse
from django.views import View, generic
from django.contrib.auth import login, views as auth_views
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render

from pokedex.forms import PokemonEditForm
from pokedex.models import Pokemon, Stat

# Create your views here.
class LoginView(auth_views.LoginView):
    template_name = "pokedex/login.html"
    next_page = "/"

class LogoutView(auth_views.LogoutView):
    next_page = "/"

class RegisterView(View):
    template_name = "pokedex/register.html"
    form_class = UserCreationForm

    def get(self, request: HttpRequest):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request: HttpRequest):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                form.cleaned_data["username"],
                password=form.cleaned_data["password1"])
            login(request, user)
            return redirect("pokedex:index")
        else:
            return render(request, self.template_name, {"form": form})

class IndexView(generic.ListView):
    template_name = "pokedex/index.html"
    context_object_name = "pokemons"

    def get_queryset(self):
        return Pokemon.objects.filter(is_deleted=False)

class PokemonView(generic.DetailView):
    queryset = Pokemon.objects.filter(is_deleted=False)
    template_name = "pokedex/pokemon_details.html"

class PokemonEditView(View):
    template_name = "pokedex/pokemon_edit.html"
    form_class = PokemonEditForm

    def get(self, request, pk):
        pokemon = get_object_or_404(Pokemon, pk=pk)

        initial_form_data = {"name": pokemon.name,}
        for i, type_ in enumerate(pokemon.types.all()):
            initial_form_data[f"type{i+1}"] = type_.pk
        for i, ability in enumerate(pokemon.abilities.all()):
            initial_form_data[f"ability{i+1}"] = ability.pk
        for stat in pokemon.stats.all():
            initial_form_data[stat.name.replace("-", "_")] = stat.base_stat

        form = self.form_class(initial_form_data)

        return render(request, self.template_name, {"pokemon": pokemon, "form": form})

    def post(self, request: HttpRequest, pk):
        pokemon = get_object_or_404(Pokemon, pk=pk)
        context = {
            "pokemon": pokemon,
            "message": "You need to login before editing a Pokemon."
        }

        if not request.user.is_authenticated:
            return render(request, self.template_name, context)

        form = self.form_class(request.POST)
        if form.is_valid():
            print(f"|| {form.cleaned_data=}")
            name = form.cleaned_data.get("name")

            if Pokemon.objects.filter(name=name).exists() and pokemon.name != name:
                form.add_error("name", f"{name} already exists. Pokemon name must be unique")
                return render(request, self.template_name, {"pokemon": pokemon, "form": form})

            pokemon.name = name
            pokemon.types.set([
                form.cleaned_data.get("type1"),
                form.cleaned_data.get("type2")
            ])
            pokemon.abilities.set([
                form.cleaned_data.get("ability1"),
                form.cleaned_data.get("ability2"),
                form.cleaned_data.get("ability3")
            ])
            for stat in ["hp", "attack", "defense", "special-attack", "special-defense", "speed"]:
                s: Stat = pokemon.stats.get(name=stat)
                s.base_stat = form.cleaned_data[stat.replace("-", "_")]
                s.save()

            pokemon.save()

            return redirect("pokedex:pokemon-detail", pk=pokemon.pk)
        else:
            return render(request, self.template_name, {"pokemon": pokemon, "form": form})

class PokemonCreateView(View):
    template_name = "pokedex/pokemon_create.html"
    form_class = PokemonEditForm

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request: HttpRequest):
        form = self.form_class(request.POST)

        if not request.user.is_authenticated:
            return render(request, self.template_name, {"message": "You need to login before creating a Pokemon."}) 

        if form.is_valid():
            name = form.cleaned_data.get("name")

            if Pokemon.objects.filter(name=name).exists():
                form.add_error("name", f"{name} already exists. Pokemon name must be unique")
                return render(request, self.template_name, {"form": form})

            pokemon = Pokemon(name=name)
            pokemon.save()

            pokemon.types.set([
                form.cleaned_data.get("type1"),
                form.cleaned_data.get("type2")
            ])

            pokemon.abilities.set([
                form.cleaned_data.get("ability1"),
                form.cleaned_data.get("ability2"),
                form.cleaned_data.get("ability3")
            ])

            Stat(pokemon=pokemon, name="hp", base_stat=form.cleaned_data.get("hp")).save()
            Stat(pokemon=pokemon, name="attack", base_stat=form.cleaned_data.get("attack")).save()
            Stat(pokemon=pokemon, name="defense", base_stat=form.cleaned_data.get("defense")).save()
            Stat(pokemon=pokemon, name="special-attack", base_stat=form.cleaned_data.get("special_attack")).save()
            Stat(pokemon=pokemon, name="special-defense", base_stat=form.cleaned_data.get("special_defense")).save()
            Stat(pokemon=pokemon, name="speed", base_stat=form.cleaned_data.get("speed")).save()

            pokemon.save()

            return redirect("pokedex:pokemon-detail", pk=pokemon.pk)
        else:
            return render(request, self.template_name, {"form": form})

class PokemonDeleteView(View):
    def post(self, request: HttpRequest, pk):
        if not request.user.is_authenticated:
            return redirect("pokedex:login")
        pokemon = get_object_or_404(Pokemon, pk=pk)
        pokemon.is_deleted = True
        pokemon.save()
        return redirect("pokedex:index")
