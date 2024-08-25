from django.db import models

# Create your models here.
class PokemonType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.name

class Ability(models.Model):
    name = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = "Abilities"

class Pokemon(models.Model):
    national_pokedex_number = models.SmallIntegerField(unique=True, blank=True, null=True)
    name = models.CharField(max_length=100, unique=True)
    sprite_slug = models.CharField(max_length=100, blank=True, null=True)
    types = models.ManyToManyField(PokemonType, through="PokemonHasType")
    abilities = models.ManyToManyField(Ability)
    is_deleted = models.BooleanField(default=False)
    def __str__(self):
        return self.name
    @property
    def nationalPokedexNum(self):
        if self.national_pokedex_number:
            return str(self.national_pokedex_number).zfill(4)
        return "custom"

class PokemonHasType(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)
    pokemon_type = models.ForeignKey(PokemonType, on_delete=models.CASCADE, blank=True, null=True)
    slot = models.SmallIntegerField()
    def __str__(self):
        return f"slot {self.slot} {self.pokemon_type}"

class Stat(models.Model):
    pokemon = models.ForeignKey(Pokemon, related_name="stats", on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    base_stat = models.SmallIntegerField()
    def __str__(self):
        return self.name
