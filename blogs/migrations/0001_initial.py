# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-02-07 22:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('image', models.ImageField(blank=True, height_field='height_field', null=True, upload_to=b'', width_field='weight_field')),
                ('height_field', models.IntegerField(default=0)),
                ('weight_field', models.IntegerField(default=0)),
                ('content', models.TextField()),
                ('updated', models.DateTimeField(auto_now=True)),
                ('timeposted', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
