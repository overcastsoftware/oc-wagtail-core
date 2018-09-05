# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import wagtail.core.fields
import wagtail.core.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('oc_core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Navigation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255)),
                ('slug', models.SlugField(max_length=255)),
                ('navigation', wagtail.core.fields.StreamField([(b'menu_block', wagtail.core.blocks.StructBlock([(b'title', wagtail.core.blocks.CharBlock()), (b'menu_items', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StreamBlock([(b'link_external', wagtail.core.blocks.StructBlock([(b'caption', wagtail.core.blocks.CharBlock()), (b'url', wagtail.core.blocks.CharBlock())])), (b'link_page', wagtail.core.blocks.PageChooserBlock())])))]))], blank=True)),
            ],
        ),
    ]
