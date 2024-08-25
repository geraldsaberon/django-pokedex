from pokedex.models import Ability, Pokemon, PokemonType, Stat, PokemonHasType

def create_pokemon(
        name: str,
        national_pokedex_number: int | None = None,
        sprite_slug: str | None = None,
        type1: PokemonType | str | None = None,
        type2: PokemonType | str | None = None,
        ability1:  Ability | str | None = None,
        ability2:  Ability | str | None = None,
        ability3:  Ability | str | None = None,
        hp: int = 0,
        attack: int = 0,
        defense: int = 0,
        special_attack: int = 0,
        special_defense: int = 0,
        speed: int = 0,
    ):
    pokemon = Pokemon(
        name=name,
        national_pokedex_number=national_pokedex_number,
        sprite_slug=sprite_slug
    )
    pokemon.save()

    type_slot_1 = PokemonHasType(pokemon=pokemon, slot=1)
    type_slot_2 = PokemonHasType(pokemon=pokemon, slot=2)

    for type_name, slot in zip([type1, type2], [type_slot_1, type_slot_2]):
        if not type_name: continue
        if not PokemonType.objects.filter(name=type_name).exists():
            PokemonType(name=type_name).save()
        slot.pokemon_type = PokemonType.objects.get(name=type_name)
        slot.save()

    for ability in [ability1, ability2, ability3]:
        if not ability: continue
        if not Ability.objects.filter(name=ability).exists():
            Ability(name=ability).save()
        pokemon.abilities.add(Ability.objects.get(name=ability))

    stat_names  = ["hp", "attack", "defense", "special-attack", "special-defense", "speed"]
    stat_values = [hp, attack, defense, special_attack, special_defense, speed]
    for stat_name, base_stat in zip(stat_names, stat_values):
        pokemon.stats.create(name=stat_name, base_stat=base_stat)

    pokemon.save()
    return pokemon

def update_pokemon(
        pokemon: Pokemon,
        name: str,
        type1: PokemonType | None = None,
        type2: PokemonType | None = None,
        ability1:  Ability | None = None,
        ability2:  Ability | None = None,
        ability3:  Ability | None = None,
        hp = 0,
        attack = 0,
        defense = 0,
        special_attack = 0,
        special_defense = 0,
        speed = 0):

    pokemon.name = name

    slot1 = PokemonHasType.objects.get(
        pokemon=pokemon,
        slot=1)
    slot1.pokemon_type = type1
    slot1.save()

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
