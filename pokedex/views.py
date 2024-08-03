from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import View, generic
from django.shortcuts import get_object_or_404, render

from pokedex.forms import PokemonEditForm
from pokedex.models import Pokemon, Stat

# Create your views here.
class IndexView(generic.ListView):
    template_name = "pokedex/index.html"
    context_object_name = "pokemons"

    def get_queryset(self):
        return Pokemon.objects.all()

class PokemonView(generic.DetailView):
    model = Pokemon
    template_name = "pokedex/pokemon_details.html"
    slug_field = "pokemon_number"
    slug_url_kwarg = "pokemon_number"

class PokemonEditView(View):
    template_name = "pokedex/pokemon_edit.html"
    form_class = PokemonEditForm

    def get(self, request, pokemon_number):
        pokemon = get_object_or_404(Pokemon, pokemon_number=pokemon_number)

        initial_form_data = {"name": pokemon.name,}
        for i, type_ in enumerate(pokemon.types.all()):
            initial_form_data[f"type{i+1}"] = type_.pk
        for i, ability in enumerate(pokemon.abilities.all()):
            initial_form_data[f"ability{i+1}"] = ability.pk
        for stat in pokemon.stat_set.all():
            initial_form_data[stat.name.replace("-", "_")] = stat.base_stat

        form = self.form_class(initial_form_data)

        return render(request, self.template_name, {"pokemon": pokemon, "form": form})

    def post(self, request, pokemon_number):
        pokemon = get_object_or_404(Pokemon, pokemon_number=pokemon_number)
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
                s: Stat = pokemon.stat_set.get(name=stat)
                s.base_stat = form.cleaned_data[stat.replace("-", "_")]
                s.save()

            pokemon.save()

            return HttpResponseRedirect(reverse("pokedex:pokemon-detail", args=[pokemon.pokeNumberId]))
        else:
            return render(request, self.template_name, {"pokemon": pokemon, "form": form})
