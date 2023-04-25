# Generated by Django 4.2 on 2023-04-19 02:23

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Draftorder',
            fields=[
                ('teamlist', models.CharField(blank=True, max_length=255, null=True)),
                ('draftyear', models.IntegerField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'draftorder',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Draftpicks',
            fields=[
                ('pickid', models.AutoField(primary_key=True, serialize=False)),
                ('draftyear', models.IntegerField()),
                ('round', models.IntegerField()),
            ],
            options={
                'verbose_name': 'Draft Pick',
                'verbose_name_plural': 'Draft Picks',
                'db_table': 'draftpicks',
                'managed': False,
            },
        ),
    ]