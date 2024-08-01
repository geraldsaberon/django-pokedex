from django.contrib import admin

from .models import Pokemon, PokemonType, Ability

# Register your models here.
admin.site.register(Pokemon)
admin.site.register(PokemonType)
admin.site.register(Ability)
