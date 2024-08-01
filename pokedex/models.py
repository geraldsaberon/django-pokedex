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
    name = models.CharField(max_length=100, unique=True)
    sprite = models.URLField()
    types = models.ManyToManyField(PokemonType)
    abilities = models.ManyToManyField(Ability)
    def __str__(self):
        return self.name

class Stat(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    base_stat = models.SmallIntegerField()
    def __str__(self):
        return self.name
