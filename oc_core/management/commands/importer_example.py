# -*- coding: utf-8 -*-
import json

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.contrib.auth.models import User
from django.utils.text import slugify

import wagtail
if wagtail.VERSION[0] >= 2:
    from wagtail.core.models import Page, Site
else:
    from wagtail.wagtailcore.models import Page, Site


from oc_core.utils import ImageImporter


class Command(BaseCommand):

    def handle(self, **options):

        self.get_json_data(options)

        # This importer simply imports under the default root page.
        # You can the move all the child pages to a different parent with a management command.
        # You can also just specify which page you want as the root here:
        #
        # root = Page.objects.get(pk=1).specific

        root = Site.objects.first().root_page.specific

        with transaction.atomic():
            for item in self.json_data:
                # Write your importer logic here.
                # Below is an example of a fictional scenario.
                # It assumes that you have a model called ItemPage
                # with tagging enabled and an image field.


                title = item["title"]
                slug = item["slug"]
                tags = item["tags"]
                image_url = item["image"]

                # We assume that the first user owns everything we import
                owner = User.objects.get(pk=1)

                self.stdout.write(u"Adding item: %s" % slugify(slug))

                item = root_page.add_child(instance=ItemPage(
                  title=title,
                  slug=slugify(slug),
                  live=True,
                  owner=owner
                ))

                self.stdout.write("Adding tags %s" % tags)
                tags_list = [t.strip() for t in tags.split(',')]
                item.tags.add(*tags_list)

                self.stdout.write("Importing image %s" % image_url)
                img_importer = ImageImporter(image_url, user=owner, tags=tags_list, title=title)

                item.image = img_importer.image
                item.save()
                item.save_revision()

                # all done.



    def get_json_data(self, options):
        json_file = options['json_file']

        try:
            with open(json_file) as data_file:
                json_data=data_file.read()
        except IOError:
            raise CommandError("The json file does not exist.")

        self.json_data = json.loads(json_data)


    def add_arguments(self, parser):
        parser.add_argument('json_file')


