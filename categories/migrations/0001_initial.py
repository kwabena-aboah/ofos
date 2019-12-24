# Generated by Django 2.1.7 on 2019-07-05 17:28

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(default=datetime.datetime.now, verbose_name='Created')),
                ('updated', models.DateTimeField(default=datetime.datetime.now, verbose_name='Updated')),
                ('is_deleted', models.BooleanField(db_index=True, default=False, verbose_name='Is deleted')),
                ('name', models.CharField(max_length=128, verbose_name='Name')),
                ('slug', models.SlugField(unique=True, verbose_name='Slug')),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
        ),
    ]