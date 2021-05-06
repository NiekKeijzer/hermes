import dataclasses
from typing import Any, Dict, Optional

import html2text
from django.template.loader import render_to_string

_converter = html2text.HTML2Text()
_converter.ignore_links = False


@dataclasses.dataclass()
class EmailBody:
    html: str
    _plain: Optional[str] = None

    def __str__(self) -> str:
        return self.html

    @property
    def plain(self) -> str:
        if self._plain is None:
            self._plain = _converter.handle(self.html)

        return self._plain


def render_email_body(
    template: str, context: Dict[str, Any], auto_plain: bool = True
) -> EmailBody:
    """
    Render the template to an email body, largely behaves as a wrapper around
     `render_to_string`.
    As HTML2Text sometimes has funky results, the `auto_plain` argument can be
     set to `False`. In which case, '.html' will be replaced with '.txt' to
     look for an alternative template to render.
    :param template: The template to render
    :param context: The context to pass to the template
    :param auto_plain: If `True` html2text is used to convert otherwise a text template is used
    :return:
    """
    html = render_to_string(template, context)

    if auto_plain:
        plain = None
    else:
        plain = render_to_string(template.replace(".html", ".txt"), context)

    return EmailBody(html, plain)
