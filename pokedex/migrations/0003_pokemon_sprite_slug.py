# Generated by Django 5.0.7 on 2024-08-01 19:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pokedex', '0002_alter_ability_options_pokemon_pokemon_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='pokemon',
            name='sprite_slug',
            field=models.CharField(default=-1, max_length=100),
            preserve_default=False,
        ),
    ]