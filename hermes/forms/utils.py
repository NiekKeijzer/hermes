import secrets


def generate_token() -> str:
    """
    Wrapper around `secrets.token_urlsafe` so it can be used as the
     default callable in models.
    :return:
    """
    return secrets.token_urlsafe(16)
