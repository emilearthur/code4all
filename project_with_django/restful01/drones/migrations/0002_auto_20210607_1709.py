# Generated by Django 3.2.4 on 2021-06-07 17:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drones', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='drone',
            name='name',
            field=models.CharField(max_length=250, unique=True),
        ),
        migrations.AlterField(
            model_name='dronecategory',
            name='name',
            field=models.CharField(max_length=250, unique=True),
        ),
        migrations.AlterField(
            model_name='pilot',
            name='name',
            field=models.CharField(max_length=150, unique=True),
        ),
    ]