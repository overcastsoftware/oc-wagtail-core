# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import wagtail
if wagtail.VERSION[0] >= 2:
    import wagtail.core.fields as fields
    import wagtail.core.blocks as blocks
else:
    import wagtail.wagtailcore.fields as fields
    import wagtail.wagtailcore.blocks as blocks


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
                ('navigation', fields.StreamField([(b'menu_block', blocks.StructBlock([(b'title', blocks.CharBlock()), (b'menu_items', blocks.ListBlock(blocks.StreamBlock([(b'link_external', blocks.StructBlock([(b'caption', blocks.CharBlock()), (b'url', blocks.CharBlock())])), (b'link_page', blocks.PageChooserBlock())])))]))], blank=True)),
            ],
        ),
    ]
