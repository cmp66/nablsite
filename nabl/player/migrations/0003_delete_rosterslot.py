# Generated by Django 4.2 on 2023-04-21 18:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('player', '0002_alter_cardedplayers_unique_together_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Rosterslot',
        ),
    ]
