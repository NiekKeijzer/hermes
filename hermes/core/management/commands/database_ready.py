import sys
from typing import Any

from django.core.management.base import BaseCommand
from django.db import connections
from django.db.utils import OperationalError


class Command(BaseCommand):
    help = "check if database is ready and accepting connections"

    def handle(self, *args: Any, **options: Any) -> None:
        default_conn = connections["default"]

        try:
            cur = default_conn.cursor()
        except OperationalError:
            sys.exit(-1)
        else:
            sys.exit(0)
