# Generated by Django 2.1.4 on 2019-02-28 23:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0003_auto_20190228_1849'),
    ]

    operations = [
        migrations.AlterField(
            model_name='food',
            name='vat',
            field=models.FloatField(default='0.36'),
        ),
    ]
