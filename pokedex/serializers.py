from rest_framework.serializers import ModelSerializer

from pokedex.models import Ability, Pokemon, PokemonType, Stat

class PokemonTypeSerializer(ModelSerializer):
    class Meta:
        model = PokemonType
        fields = ["name"]

class AbilitySerializer(ModelSerializer):
    class Meta:
        model = Ability
        fields = ["name"]

class StatSerializer(ModelSerializer):
    class Meta:
        model = Stat
        fields = ["name", "base_stat"]

class PokemonSerializer(ModelSerializer):
    types = PokemonTypeSerializer(many=True)
    abilities = AbilitySerializer(many=True)
    stats = StatSerializer(many=True)

    class Meta:
        model = Pokemon
        fields = [
            "id",
            "name",
            "national_pokedex_number",
            "types",
            "abilities",
            "stats"
        ]
