from pokedex.models import Ability, Pokemon, PokemonType, Stat, PokemonHasType

def create_pokemon(
        name: str,
        type1: PokemonType | str | None = None,
        type2: PokemonType | str | None = None,
        ability1:  Ability | str | None = None,
        ability2:  Ability | str | None = None,
        ability3:  Ability | str | None = None,
        hp = 0,
        attack = 0,
        defense = 0,
        special_attack = 0,
        special_defense = 0,
        speed = 0,
    ):
    pokemon = Pokemon(name=name)
    pokemon.save()

    type1    = get_model_from_str(type1, PokemonType) if type1    else None
    type2    = get_model_from_str(type2, PokemonType) if type2    else None
    ability1 = get_model_from_str(ability1,  Ability) if ability1 else None
    ability2 = get_model_from_str(ability2,  Ability) if ability2 else None
    ability3 = get_model_from_str(ability3,  Ability) if ability3 else None

    if type1: PokemonHasType(pokemon=pokemon, pokemon_type=type1, slot=1).save()
    if type2: PokemonHasType(pokemon=pokemon, pokemon_type=type2, slot=2).save()

    pokemon.abilities.set([ability1, ability2, ability3])

    stat_names  = ["hp", "attack", "defense", "special-attack", "special-defense", "speed"]
    stat_values = [hp, attack, defense, special_attack, special_defense, speed]
    for stat_name, stat_value in zip(stat_names, stat_values):
        Stat(pokemon=pokemon, name=stat_name, base_stat=stat_value).save()

    pokemon.save()
    return pokemon


def get_model_from_str(s, model):
    """
    Return an object from 'model' with name=s
    if s is a string
    """
    if type(s) == str:
        return model.objects.get(name=s)
    return s


def update_pokemon(
        pokemon: Pokemon,
        name: str,
        type1: PokemonType | str | None = None,
        type2: PokemonType | str | None = None,
        ability1:  Ability | str | None = None,
        ability2:  Ability | str | None = None,
        ability3:  Ability | str | None = None,
        hp = 0,
        attack = 0,
        defense = 0,
        special_attack = 0,
        special_defense = 0,
        speed = 0):

    pokemon.name = name

    if type1:
        slot1 = PokemonHasType.objects.get(
            pokemon=pokemon,
            slot=1)
        slot1.pokemon_type = type1
        slot1.save()

    if type2:
        slot2 = PokemonHasType.objects.get(
            pokemon=pokemon,
            slot=2)
        slot2.pokemon_type = type2
        slot2.save()

    pokemon.abilities.set([
        ability1,
        ability2,
        ability3
    ])

    stat_name = ["hp", "attack", "defense", "special-attack", "special-defense", "speed"]
    stat_values = [hp, attack, defense, special_attack, special_defense, speed]
    for stat_name, stat_value in zip(stat_name, stat_values):
        s: Stat = pokemon.stats.get(name=stat_name)
        s.base_stat = stat_value
        s.save()

    pokemon.save()
    return pokemon
