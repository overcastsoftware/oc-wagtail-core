# -*- coding: utf-8 -*-
import os
import urllib2
import requests
from django.core.files import File
from willow.image import Image as WillowImage

import wagtail
if wagtail.VERSION[0] >= 2:
    from wagtail.images.models import get_image_model
    from wagtail.images.forms import get_image_form
    from wagtail.images.fields import ALLOWED_EXTENSIONS
else:
    from wagtail.wagtailimages.models import get_image_model
    from wagtail.wagtailimages.forms import get_image_form
    from wagtail.wagtailimages.fields import ALLOWED_EXTENSIONS


class ImageImporter(object):

    def __init__(self, image_url, scrape_dir='scrape_images', user=None, title=None, tags=[]):

        self.tags = tags
        self.title = title
        self.user = user
        self.scrape_dir = scrape_dir
        self.image_url = self.to_unicode_or_bust(image_url)
        self.decoded_url = self.decode_url()
        self.filename = self.get_filename_from_url()

        if self.title is  None:
            self.title = self.filename


        Image = get_image_model()

        try:
            self.image = Image.objects.get(title=self.title)
        except Image.DoesNotExist:
            print u"Getting image"
            tmp_image = self.get_image()
            self.image = self.save_image(tmp_image)
        except Image.MultipleObjectsReturned:
            print u"Found multiple images, using first"
            self.image = Image.objects.filter(title=self.title).first()
        else:
            print u"Found image in database"

        self.add_tags()


    def add_tags(self):
        if self.tags != []:
            print u"Tagging image"
            self.image.tags.add(*self.tags)
            self.image.save()


    def decode_url(self):
        #print url
        #print repr(urllib2.unquote(url))
        return urllib2.unquote(self.image_url)


    def get_filename_from_url(self):
        return self.decoded_url.split('/')[-1]


    def get_image(self):
        image_dir = self.scrape_dir
        fname = self.filename.encode('utf8')
        fname_to_write = os.path.join(image_dir, fname)
        print "fname_to_write", fname_to_write

        if os.path.exists(fname_to_write):
            print "Found image in scrapedir, skipping."
        else:
            print "Fetching image from url: %s" % self.decoded_url
            img = requests.get(self.decoded_url)

            if not os.path.exists(image_dir):
                os.makedirs(image_dir)
            with open(fname_to_write, 'w') as f:
                f.write(img.content)

        return fname_to_write


    def is_bmp_format(self, file_path):
        return file_path.split('.')[-1] in ["bmp"]


    def convert_bmp_image(self, file_path):
        new_file_path = file_path.replace("bmp", "jpg")
        with open(file_path, 'rb') as f:
            img = WillowImage.open(f)
            output = open(new_file_path, 'wb')
            img.save_as_jpeg(output)
            output.close()
            return new_file_path


    def save_image(self, file_path):
        Image = get_image_model()
        ImageForm = get_image_form(Image)

        if self.is_bmp_format(file_path):
            file_path = self.convert_bmp_image(file_path)

        f=open(file_path, 'r')
        myfile = File(f)


        form = ImageForm({'title': self.title}, {'file': myfile})

        #form.is_valid() == True
        image = form.save(commit=False)
        if self.user is not None:
            image.uploaded_by_user = self.user
        image.save()

        return image


    def to_unicode_or_bust(self, obj, encoding='utf-8'):
        if isinstance(obj, basestring):
            if not isinstance(obj, unicode):
                obj = unicode(obj, encoding)
        return obj


# test
# from wagtail.images.models import get_image_model
# Image = get_image_model()
# from oc_core.utils import ImageImporter
# importer = ImageImporter("http://static.guim.co.uk/sys-images/Guardian/Pix/pictures/2014/4/11/1397210130748/Spring-Lamb.-Image-shot-2-011.jpg", title=u"Lamb að hoppa", tags=[u"Lamb", u"Hoppa", u"Draumur"])