# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import wagtail.wagtailcore.fields
import wagtail.wagtailcore.blocks


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
                ('navigation', wagtail.wagtailcore.fields.StreamField([(b'menu_block', wagtail.wagtailcore.blocks.StructBlock([(b'title', wagtail.wagtailcore.blocks.CharBlock()), (b'menu_items', wagtail.wagtailcore.blocks.ListBlock(wagtail.wagtailcore.blocks.StreamBlock([(b'link_external', wagtail.wagtailcore.blocks.StructBlock([(b'caption', wagtail.wagtailcore.blocks.CharBlock()), (b'url', wagtail.wagtailcore.blocks.CharBlock())])), (b'link_page', wagtail.wagtailcore.blocks.PageChooserBlock())])))]))], blank=True)),
            ],
        ),
    ]
