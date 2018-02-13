# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-02-12 02:08
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cms', '0019_auto_20180212_1208'),
    ]

    operations = [
        migrations.CreateModel(
            name='Hello',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, related_name='vote_app_hello', serialize=False, to='cms.CMSPlugin')),
                ('guest_name', models.CharField(default='Guest', max_length=50)),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
    ]
