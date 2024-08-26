from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User, Permission
from rest_framework.test import APITestCase
from rest_framework import status

from pokedex.models import Pokemon
from pokedex.forms import PokemonEditForm as PokemonForm
from pokedex.utils import create_pokemon

from . import sample_valid_form_data, sample_valid_api_data

# Create your tests here.
class SetUpBase:
    @classmethod
    def setUpTestData(cls):
        user = User(username="user")
        user.set_password("123")
        user.save()
        user.user_permissions.set([
            Permission.objects.get(codename="add_pokemon"),
            Permission.objects.get(codename="view_pokemon"),
            Permission.objects.get(codename="change_pokemon"),
            Permission.objects.get(codename="delete_pokemon"),
        ])

    def setUp(self):
        self.test_pokemon = create_pokemon(
            name="bulbasaur",
            type1="grass",
            type2="poison",
            ability1="overgrow",
            ability2="chlorophyll",
            hp = 0,
            attack = 0,
            defense = 0,
            special_attack = 0,
            special_defense = 0,
            speed = 0
        )

class PokemonFormTests(SetUpBase, TestCase):
    def test_create_pokemon(self):
        form = PokemonForm(sample_valid_form_data)
        self.assertTrue(form.is_valid())
        pokemon = create_pokemon(**form.cleaned_data)
        self.assertEqual(Pokemon.objects.count(), 2)
        self.assertEqual(pokemon.name, sample_valid_form_data["name"])
        self.assertEqual(pokemon.types.count(), 2)
        self.assertEqual(pokemon.abilities.count(), 2)

class PokedexAPITests(SetUpBase, APITestCase):
    def test_pokemon_list(self):
        response = self.client.get(reverse("pokedex:api-pokemon-list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["count"], 1)

    def test_fetch_pokemon_details(self):
        url = reverse("pokedex:api-pokemon-detail", args=(self.test_pokemon.pk,))
        response = self.client.get(url, sample_valid_api_data, format="json")
        json = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json["name"], self.test_pokemon.name)

    def test_create_pokemon_without_auth(self):
        response = self.client.post(reverse("pokedex:api-pokemon-list"), sample_valid_api_data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Pokemon.objects.count(), 1)

    def test_create_pokemon(self):
        logged_in = self.client.login(username="user", password="123")
        self.assertTrue(logged_in)

        url = reverse("pokedex:api-pokemon-list")
        response = self.client.post(url, sample_valid_api_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Pokemon.objects.count(), 2)

    def test_update_pokemon(self):
        logged_in = self.client.login(username="user", password="123")
        self.assertTrue(logged_in)

        url = reverse("pokedex:api-pokemon-detail", args=(self.test_pokemon.pk,))
        data = {"name": "bulbasaurus"}
        response = self.client.patch(url, data)
        json = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json["name"], data["name"])

    def test_delete_pokemon(self):
        logged_in = self.client.login(username="user", password="123")
        self.assertTrue(logged_in)

        url = reverse("pokedex:api-pokemon-detail", args=(self.test_pokemon.pk,))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.test_pokemon.refresh_from_db()
        self.assertTrue(self.test_pokemon.is_deleted)
