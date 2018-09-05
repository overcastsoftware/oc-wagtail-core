from django.db import models

import wagtail
if wagtail.VERSION[0] >= 2:
    from wagtail.core.models import Page, Orderable
    from wagtail.core.fields import RichTextField, StreamField
    from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel, MultiFieldPanel, InlinePanel
    from wagtail.images.edit_handlers import ImageChooserPanel
    from wagtail.search import index
    from wagtail.core import blocks
    from wagtail.snippets.models import register_snippet
else:
    from wagtail.core.models import Page, Orderable
    from wagtail.core.fields import RichTextField, StreamField
    from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel, MultiFieldPanel, InlinePanel
    from wagtail.images.edit_handlers import ImageChooserPanel
    from wagtail.search import index
    from wagtail.core import blocks
    from wagtail.snippets.models import register_snippet

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

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
    ]

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

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
    ]

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
