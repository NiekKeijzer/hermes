import secrets
from typing import Dict, List, Union

import bleach


def generate_token() -> str:
    """
    Wrapper around `secrets.token_urlsafe` so it can be used as the
     default callable in models.
    :return:
    """
    return secrets.token_urlsafe(16)


_FormData = Dict[str, Union[str, List[str]]]


def sanitize_and_flatten(data: _FormData) -> _FormData:
    sanitized = {}
    for key, value in data.items():
        key = bleach.clean(key)

        if isinstance(value, list):
            value = [bleach.linkify(bleach.clean(v)) for v in value]
            if len(value) == 1:
                value = value[0]
        else:
            value = bleach.clean(value)

        sanitized[key] = value

    return sanitized
