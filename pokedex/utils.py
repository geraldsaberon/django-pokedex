from pokedex.models import Ability, Pokemon, PokemonType, Stat

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

    pokemon.types.set([type1, type2])
    pokemon.abilities.set([ability1, ability2, ability3])

    ability_names  = ["hp", "attack", "defense", "special-attack", "special-defense", "speed"]
    ability_values = [hp, attack, defense, special_attack, special_defense, speed]
    for name, base_stat in zip(ability_names, ability_values):
        Stat(pokemon=pokemon, name=name, base_stat=base_stat).save()

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
