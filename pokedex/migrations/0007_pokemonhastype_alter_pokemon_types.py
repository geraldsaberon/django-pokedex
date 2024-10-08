# Generated by Django 5.0.7 on 2024-08-10 20:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pokedex', '0006_rename_pokemon_number_pokemon_national_pokedex_number_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='PokemonHasType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slot', models.SmallIntegerField()),
                ('pokemon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pokedex.pokemon')),
                ('pokemon_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pokedex.pokemontype')),
            ],
        ),
        migrations.RemoveField(
            model_name="pokemon",
            name="types",
        ),
        migrations.AddField(
            model_name='pokemon',
            name='types',
            field=models.ManyToManyField(through='pokedex.PokemonHasType', to='pokedex.pokemontype'),
        ),
    ]
