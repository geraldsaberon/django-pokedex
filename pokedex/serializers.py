from rest_framework.serializers import ChoiceField, ModelSerializer, CharField, ValidationError

from pokedex.models import Ability, Pokemon, PokemonHasType, PokemonType, Stat

class PokemonTypeSerializer(ModelSerializer):
    name = CharField()
    class Meta:
        model = PokemonType
        fields = ["name"]
    def validate_name(self, pokemon_type):
        if PokemonType.objects.filter(name=pokemon_type).exists():
            return pokemon_type
        else:
            raise ValidationError(f"{pokemon_type} is not a valid pokemon type")

class PokemonHasTypeSerializer(ModelSerializer):
    type = PokemonTypeSerializer(source="pokemon_type")
    slot = ChoiceField(choices=(1, 2))
    class Meta:
        model = PokemonHasType
        fields = ["type", "slot"]

class AbilitySerializer(ModelSerializer):
    name = CharField()
    class Meta:
        model = Ability
        fields = ["name"]
    def validate_name(self, pokemon_ability):
        if Ability.objects.filter(name=pokemon_ability).exists():
            return pokemon_ability
        else:
            raise ValidationError(f"{pokemon_ability} is not a valid pokemon ability")

class StatSerializer(ModelSerializer):
    class Meta:
        model = Stat
        fields = ["name", "base_stat"]

class PokemonSerializer(ModelSerializer):
    types = PokemonHasTypeSerializer(many=True, source="pokemonhastype_set")
    abilities = AbilitySerializer(many=True)
    stats = StatSerializer(many=True)

    def create(self, validated_data):
        pokemon = Pokemon(name=validated_data["name"])
        pokemon.save()

        for t in validated_data["pokemonhastype_set"]:
            type_ = t["pokemon_type"]["name"]
            slot =  t["slot"]
            PokemonHasType(
                pokemon=pokemon,
                pokemon_type=PokemonType.objects.get(name=type_),
                slot=slot
            ).save()

        for ability in validated_data["abilities"]:
            pokemon.abilities.add(
                Ability.objects.get(name=ability["name"])
            )

        for stat in validated_data["stats"]:
            Stat(pokemon=pokemon, name=stat["name"], base_stat=stat["base_stat"]).save()

        pokemon.save()
        return pokemon

    def update(self, instance: Pokemon, validated_data):
        if "name" in validated_data:
            instance.name = validated_data["name"]
        if "pokemonhastype_set" in validated_data:
            for t in validated_data["pokemonhastype_set"]:
                type_name = t["pokemon_type"]["name"]
                slot = t["slot"]
                pht = PokemonHasType.objects.get(
                    pokemon=instance,
                    slot=slot
                )
                pht.pokemon_type = PokemonType.objects.get(name=type_name)
                pht.save()

        if "abilities" in validated_data:
            instance.abilities.clear()
            for a in validated_data["abilities"]:
                ability = Ability.objects.get(name=a["name"])
                instance.abilities.add(ability)

        if "stats" in validated_data:
            for stat in validated_data["stats"]:
                stat_name = stat["name"]
                base_stat = stat["base_stat"]
                s: Stat = instance.stats.get(name=stat_name)
                s.base_stat = base_stat
                s.save()
        instance.save()
        return instance

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
        read_only_fields = ["id", "national_pokedex_number"]
