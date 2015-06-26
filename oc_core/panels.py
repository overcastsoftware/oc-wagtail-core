from django.conf import settings
from django.utils.safestring import mark_safe

from wagtail.wagtailadmin.edit_handlers import BaseFieldPanel


#https://gist.github.com/alej0varas/64e07b1f585f46f0fab2

class ColorFieldPanel(object):
    def __init__(self, field_name, classname=None):
        self.field_name = field_name
        self.classname = classname

    def bind_to_model(self, model):
        return type(str('_ColorFieldPanel'), (BaseFieldPanel,), {
            'model': model,
            'field_name': self.field_name,
            'classname': self.classname,
        })