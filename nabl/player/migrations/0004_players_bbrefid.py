# Generated by Django 4.2 on 2023-04-21 18:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('player', '0003_delete_rosterslot'),
    ]

    operations = [
        migrations.AddField(
            model_name='players',
            name='bbrefid',
            field=models.CharField(blank=True, max_length=16, null=True),
        ),
    ]