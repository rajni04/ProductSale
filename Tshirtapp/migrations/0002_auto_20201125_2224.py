# Generated by Django 3.0.5 on 2020-11-25 16:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Tshirtapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tshirt',
            name='slug',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
