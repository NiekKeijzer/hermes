from typing import Any

from django import template
from django.http import HttpRequest
from django.shortcuts import reverse
from django.template.base import NodeList, Parser, Token
from django.template.context import Context, RequestContext

register = template.Library()


@register.simple_tag(takes_context=True)
def absolute_url(
    context: RequestContext, view_name: str, *args: Any, **kwargs: Any
) -> str:
    request: HttpRequest = context["request"]

    return request.build_absolute_uri(reverse(view_name, args=args, kwargs=kwargs))


@register.filter(name="dict_key")
def dict_key(data: dict, key: str, default: Any = None) -> Any:
    return data.get(key, default)


class CaptureasNode(template.Node):
    def __init__(self, nodelist: NodeList, varname: str):
        self.nodelist = nodelist
        self.varname = varname

    def render(self, context: Context) -> str:
        output = self.nodelist.render(context)
        context[self.varname] = output

        return ""


@register.tag(name="captureas")
def do_captureas(parser: Parser, token: Token) -> CaptureasNode:
    try:
        tag_name, args = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError("'captureas' node requires a variable name.")
    nodelist = parser.parse(("endcaptureas",))
    parser.delete_first_token()

    return CaptureasNode(nodelist, args)
