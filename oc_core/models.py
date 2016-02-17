from django.db import models

from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailcore.fields import RichTextField, StreamField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, StreamFieldPanel, MultiFieldPanel, InlinePanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailsearch import index
from wagtail.wagtailcore import blocks
from wagtail.wagtailsnippets.models import register_snippet

from modelcluster.fields import ParentalKey

from .mixins import RelatedLinkMixin, CarouselItemMixin


# Standard index page

class StandardIndexPageRelatedLink(Orderable, RelatedLinkMixin):
    page = ParentalKey('StandardIndexPage', related_name='related_links')


class StandardIndexPage(Page):
    intro = RichTextField(blank=True)
    feed_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    search_fields = Page.search_fields + (
        index.SearchField('intro'),
    )

StandardIndexPage.content_panels = [
    FieldPanel('title', classname="full title"),
    FieldPanel('intro', classname="full"),
    InlinePanel('related_links', label="Related links"),
]

StandardIndexPage.promote_panels = Page.promote_panels + [
    ImageChooserPanel('feed_image'),
]


# Standard page

class StandardPageCarouselItem(Orderable, CarouselItemMixin):
    page = ParentalKey('StandardPage', related_name='carousel_items')


class StandardPageRelatedLink(Orderable, RelatedLinkMixin):
    page = ParentalKey('StandardPage', related_name='related_links')


class StandardPage(Page):
    intro = RichTextField(blank=True)
    body = RichTextField(blank=True)
    feed_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    search_fields = Page.search_fields + (
        index.SearchField('intro'),
        index.SearchField('body'),
    )

StandardPage.content_panels = [
    FieldPanel('title', classname="full title"),
    FieldPanel('intro', classname="full"),
    InlinePanel('carousel_items', label="Carousel items"),
    FieldPanel('body', classname="full"),
    InlinePanel('related_links', label="Related links"),
]

StandardPage.promote_panels = Page.promote_panels + [
    ImageChooserPanel('feed_image'),
]



class Navigation(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    navigation = StreamField([
        ('menu_block', blocks.StructBlock([
            ('title', blocks.CharBlock()),
            ('menu_items', blocks.ListBlock(blocks.StreamBlock([
                ('link_external', blocks.StructBlock([
                        ('caption', blocks.CharBlock()),
                        ('url', blocks.CharBlock()),
                    ])),
                ('link_page', blocks.PageChooserBlock()),
                ('mega_menu', blocks.BooleanBlock(label="Show_in_mega_menu", default=False, blank=True, required=False)),
            ])))])),
    ], blank=True)

    panels = [
        FieldPanel('title'),
        FieldPanel('slug'),
        StreamFieldPanel('navigation'),
    ]

    def __unicode__(self):
        return self.title

register_snippet(Navigation)