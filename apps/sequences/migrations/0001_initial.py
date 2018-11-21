# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2018-11-21 17:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Sequence',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('code', models.CharField(max_length=100, unique=True, verbose_name='Code')),
                ('value', models.PositiveIntegerField(default=0, verbose_name='Value')),
            ],
            options={
                'ordering': ('code',),
            },
        ),
    ]