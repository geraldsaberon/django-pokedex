from pathlib import Path
from shutil import copyfileobj
import os

from django.core.management.base import BaseCommand
from django.db import IntegrityError
import requests

from ...models import Ability, Pokemon, PokemonType


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

                name = res_json["name"]
                sprite = res_json["sprites"]["front_default"]
                abilities = [row["ability"]["name"] for row in res_json["abilities"]]
                types = [row["type"]["name"] for row in res_json["types"]]
                stats = [(row["stat"]["name"], row["base_stat"]) for row in res_json["stats"]]

                print(f"|| name: {name}")
                print(f"|| || sprite: {sprite}")
                print(f"|| || abilities: {abilities}")
                print(f"|| || types: {types}")
                print(f"|| || stats: ", end="")
                for stat in stats:
                    print(f"{stat[0]}={stat[1]} ", end="")
                print(f"\n|| ||")

                image_res = requests.get(sprite, stream=True)
                if image_res.status_code == 200:
                    with open(sprite_save_path/f"{sprite.rsplit("/", 1)[1]}", "wb") as f:
                        copyfileobj(image_res.raw, f)

                p = Pokemon(name=name, sprite=sprite_save_path)
                p.save()

                for ability in abilities:
                    try:
                        p.abilities.create(name=ability)
                    except IntegrityError: # ability already exists in db
                        p.abilities.add(Ability.objects.get(name=ability))
                for type_ in types:
                    try:
                        p.types.create(name=type_)
                    except IntegrityError: # type already exists in db
                        p.types.add(PokemonType.objects.get(name=type_))
                for stat_name, base_stat in stats:
                    p.stat_set.create(name=stat_name, base_stat=base_stat)

                p.save()
