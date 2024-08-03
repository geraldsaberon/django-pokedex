from django import forms

from pokedex.models import Ability, PokemonType

class PokemonEditForm(forms.Form):
    name = forms.CharField(max_length=100)

    type1 = forms.ModelChoiceField(
        queryset=PokemonType.objects.order_by("name"),
        required=True,
        label="Type")
    type2 = forms.ModelChoiceField(
        queryset=PokemonType.objects.order_by("name"),
        required=False,
        label="Type")

    ability1 = forms.ModelChoiceField(
        queryset=Ability.objects.order_by("name"),
        required=True,
        label="Ability")
    ability2 = forms.ModelChoiceField(
        queryset=Ability.objects.order_by("name"),
        required=False,
        label="Ability")
    ability3 = forms.ModelChoiceField(
        queryset=Ability.objects.order_by("name"),
        required=False,
        label="Ability")

    hp              = forms.IntegerField(min_value=0)
    attack          = forms.IntegerField(min_value=0)
    defense         = forms.IntegerField(min_value=0)
    special_attack  = forms.IntegerField(min_value=0)
    special_defense = forms.IntegerField(min_value=0)
    speed           = forms.IntegerField(min_value=0)
