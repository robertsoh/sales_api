# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-12-13 21:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='city',
            field=models.CharField(max_length=255, null=True, verbose_name='City'),
        ),
        migrations.AddField(
            model_name='order',
            name='email',
            field=models.EmailField(max_length=254, null=True, verbose_name='Email'),
        ),
        migrations.AddField(
            model_name='order',
            name='full_name',
            field=models.CharField(max_length=255, null=True, verbose_name='Full name'),
        ),
        migrations.AddField(
            model_name='order',
            name='has_shipping',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='order',
            name='phone',
            field=models.CharField(max_length=20, null=True, verbose_name='Phone'),
        ),
        migrations.AddField(
            model_name='order',
            name='street',
            field=models.CharField(max_length=255, null=True, verbose_name='Address'),
        ),
    ]
