# Generated by Django 5.0.7 on 2024-08-25 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pokedex', '0008_alter_pokemonhastype_pokemon_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pokemon',
            name='sprite',
        ),
        migrations.AlterField(
            model_name='pokemon',
            name='sprite_slug',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
