# Generated by Django 4.2 on 2023-04-26 00:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('league', '0003_divisions_leagueid_emailaddresses_memberid_and_more'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='emailaddresses',
            constraint=models.UniqueConstraint(fields=('memberid', 'primaryaddress'), name='unique_primaryaddress'),
        ),
        migrations.AddConstraint(
            model_name='phonenumbers',
            constraint=models.UniqueConstraint(fields=('memberid', 'phonenumber'), name='unique_phonenumber'),
        ),
    ]