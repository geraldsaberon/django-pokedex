# Generated by Django 5.0.7 on 2024-08-19 19:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pokedex', '0007_pokemonhastype_alter_pokemon_types'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pokemonhastype',
            name='pokemon_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='pokedex.pokemontype'),
        ),
    ]
