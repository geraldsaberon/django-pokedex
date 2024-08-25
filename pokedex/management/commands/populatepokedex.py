from pathlib import Path
from shutil import copyfileobj
import os

from django.core.management.base import BaseCommand
import requests

from ...models import Ability, Pokemon, PokemonType
from ...utils import create_pokemon

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
                res_json: dict = res.json()

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

                types = {"type1": None, "type2": None}
                for a in res_json.get("types", []):
                    types[ f"type{a['slot']}" ] = a["type"]["name"]

                abilities = [None, None, None]
                for i, a in enumerate(res_json.get("abilities", [])):
                    abilities[i] = a["ability"]["name"]

                stats = {}
                for s in res_json.get("stats", []):
                    stats[ s["stat"]["name"].replace("-", "_") ] = s["base_stat"]

                create_pokemon(
                    name = name,
                    national_pokedex_number = pokemon_id,
                    sprite_slug = sprite_slug,
                    ability1 = abilities[0],
                    ability2 = abilities[1],
                    ability3 = abilities[2],
                    **types,
                    **stats
                )
