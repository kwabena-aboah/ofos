# Generated by Django 2.1.4 on 2019-02-28 08:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='food',
            name='vat',
            field=models.FloatField(default='0.0'),
        ),
    ]
