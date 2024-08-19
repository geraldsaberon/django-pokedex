from pathlib import Path
from shutil import copyfileobj
import os

from django.core.management.base import BaseCommand
from django.db import IntegrityError
import requests

from ...models import Ability, Pokemon, PokemonHasType, PokemonType


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        Pokemon.objects.all().delete()
        Ability.objects.all().delete()
        PokemonType.objects.all().delete()

        sprite_save_path = Path(__file__).parent.parent.parent / "static/pokemon-sprites"
        if not os.path.isdir(sprite_save_path):
            print("Sprite save path does not exist. Making directory...")
            os.makedirs(sprite_save_path)

        for i in range(1, 152): # only gen 1 (1-151) for now
            res = requests.get(f"https://pokeapi.co/api/v2/pokemon/{i}")
            if res.status_code == 200:
                res_json = res.json()

                pokemon_id = res_json["id"]
                name = res_json["name"]
                sprite = res_json["sprites"]["front_default"]
                sprite_slug = f"/static/pokemon-sprites/{os.path.split(sprite)[1]}"
                abilities = [row["ability"]["name"] for row in res_json["abilities"]]
                types = [row["type"]["name"] for row in res_json["types"]]
                stats = [(row["stat"]["name"], row["base_stat"]) for row in res_json["stats"]]

                print(f"|| {str(pokemon_id).zfill(4)} {name} ")
                print(f"|| || sprite: {sprite}")
                print(f"|| || abilities: {abilities}")
                print(f"|| || types: {types}")
                print(f"|| || stats: ", end="")
                for stat in stats:
                    print(f"{stat[0]}={stat[1]} ", end="")
                print(f"\n|| ||")

                image_res = requests.get(sprite, stream=True)
                sprite_file = sprite_save_path / os.path.split(sprite)[1]
                if image_res.status_code == 200:
                    with open(sprite_file, "wb") as f:
                        copyfileobj(image_res.raw, f)

                p = Pokemon(
                    national_pokedex_number=pokemon_id,
                    name=name,
                    sprite=sprite_file,
                    sprite_slug=sprite_slug)
                p.save()


                type_1 = PokemonHasType(pokemon=p, slot=1)
                type_2 = PokemonHasType(pokemon=p, slot=2)

                for type_name, slot in zip(types, [type_1, type_2]):
                    if not PokemonType.objects.filter(name=type_name).exists():
                        PokemonType(name=type_name).save()
                    slot.pokemon_type = PokemonType.objects.get(name=type_name)

                for ability in abilities:
                    try:
                        p.abilities.create(name=ability)
                    except IntegrityError: # ability already exists in db
                        p.abilities.add(Ability.objects.get(name=ability))

                for stat_name, base_stat in stats:
                    p.stats.create(name=stat_name, base_stat=base_stat)

                type_1.save()
                type_2.save()
                p.save()
