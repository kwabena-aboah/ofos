# Generated by Django 2.1.4 on 2019-02-28 18:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0002_food_vat'),
    ]

    operations = [
        migrations.AlterField(
            model_name='food',
            name='vat',
            field=models.FloatField(default='0.03'),
        ),
    ]
