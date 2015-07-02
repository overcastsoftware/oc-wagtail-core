from django.db import models

from wagtail.wagtailadmin.edit_handlers import FieldPanel, MultiFieldPanel, \
    PageChooserPanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtaildocs.edit_handlers import DocumentChooserPanel
from wagtail.wagtailcore.models import Page


class CustomTemplateMixin(models.Model):
    """
    Allows per-instance templates.
    """
    template_name = models.CharField('Template Name', max_length=100, blank=True)

    class Meta(object):
        abstract = True

    def get_template(self, request, *args, **kwargs):
        """
        Returns template name.
        """
        if self.template_name:
            return self.template_name

        # Fall back to standard page method.
        return Page.get_template(self, request, *args, **kwargs)


class LinkFieldsMixin(models.Model):
    link_external = models.URLField("External link", blank=True)
    link_page = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        related_name='+'
    )
    link_document = models.ForeignKey(
        'wagtaildocs.Document',
        null=True,
        blank=True,
        related_name='+'
    )

    @property
    def link(self):
        if self.link_page:
            return self.link_page.url
        elif self.link_document:
            return self.link_document.url
        else:
            return self.link_external

    panels = [
        FieldPanel('link_external'),
        PageChooserPanel('link_page'),
        DocumentChooserPanel('link_document'),
    ]

    class Meta:
        abstract = True


# Carousel items
class CarouselItemMixin(LinkFieldsMixin):
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    embed_url = models.URLField("Embed URL", blank=True)
    caption = models.CharField(max_length=255, blank=True)

    panels = [
        ImageChooserPanel('image'),
        FieldPanel('embed_url'),
        FieldPanel('caption'),
        MultiFieldPanel(LinkFieldsMixin.panels, "Link"),
    ]

    class Meta:
        abstract = True


# Related links

class RelatedLinkMixin(LinkFieldsMixin):
    title = models.CharField(max_length=255, help_text="Link title")

    panels = [
        FieldPanel('title'),
        MultiFieldPanel(LinkFieldsMixin.panels, "Link"),
    ]

    class Meta:
        abstract = True
