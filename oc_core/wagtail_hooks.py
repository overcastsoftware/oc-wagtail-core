import wagtail
if wagtail.VERSION[0] >= 2:
    from wagtail.core import hooks
else:
    from wagtail.wagtailcore import hooks
from django.conf import settings
from django.utils.html import format_html_join


@hooks.register('insert_editor_js')
def editor_js():
    """
    Add extra JS files to the admin
    """
    js_files = [
        'oc_core/js/spectrum.js',
    ]
    js_includes = format_html_join(
        '\n',
        '<script type="text/javascript" src="{0}{1}"></script>',
        ((settings.STATIC_URL, filename) for filename in js_files)
    )

    return js_includes

@hooks.register('insert_editor_css')
def editor_css():

    css_files = [
        'oc_core/css/spectrum.css',
    ]
    css_includes = format_html_join(
        '\n',
        '<link rel="stylesheet" href="{0}{1}">',
        ((settings.STATIC_URL, filename) for filename in css_files)
    )

    return css_includes