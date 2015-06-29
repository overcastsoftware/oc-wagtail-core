# -*- coding: utf-8 -*-
import os
import urllib2
import requests
from wagtail.wagtailimages.models import get_image_model
from wagtail.wagtailimages.forms import get_image_form
from django.core.files import File


class ImageImporter(object):

    def __init__(self, image_url, scrape_dir='scrape_images', user=None, title=None, tags=[]):

        self.tags = tags
        self.title = title
        self.user = user
        self.scrape_dir = scrape_dir
        self.image_url = self.to_unicode_or_bust(image_url)
        self.decoded_url = self.decode_url()
        self.filename = self.get_filename_from_url()

        Image = get_image_model()

        try:
            self.image = Image.objects.get(title=self.filename)
        except Image.DoesNotExist:
            print u"Fetching image from url"
            tmp_image = self.get_image()
            self.image = self.save_image(tmp_image)
        except Image.MultipleObjectsReturned:
            print u"Found multiple images, using first"
            self.image = Image.objects.filter(title=get_filename_from_url(decode_url(image_url))).first()
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
      return urllib2.unquote(self.image_url).encode('latin-1').decode('utf8')

    def get_filename_from_url(self):
      return self.decoded_url.split('/')[-1]

    def get_image(self):
      image_dir = self.scrape_dir
      img = requests.get(self.decoded_url)
      fname = self.filename.encode('utf8')
      #print "Fetching image: %s" % fname
      fname_to_write = os.path.join(image_dir, fname)
      print "fname_to_write"
      print fname_to_write
      if not os.path.exists(image_dir):
        os.makedirs(image_dir)
      with open(fname_to_write, 'w') as f:
        f.write(img.content)
        #print "... wrote %s" % fname_to_write
        return fname_to_write

    def save_image(self, file_path):
        Image = get_image_model()
        ImageForm = get_image_form(Image)

        f=open(file_path, 'r')
        myfile = File(f)

        if self.title is  None:
            self.title = self.filename

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
# from wagtail.wagtailimages.models import get_image_model
# Image = get_image_model()
# from oc_core.utils import ImageImporter
# importer = ImageImporter("http://static.guim.co.uk/sys-images/Guardian/Pix/pictures/2014/4/11/1397210130748/Spring-Lamb.-Image-shot-2-011.jpg", title=u"Lamb að hoppa", tags=[u"Lamb", u"Hoppa", u"Draumur"])