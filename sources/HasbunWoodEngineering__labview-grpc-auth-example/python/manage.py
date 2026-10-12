#!/usr/bin/env python
"""Project management entrypoint for Django CLI commands.

Sets the default settings module and delegates to Django's command runner so
`manage.py <command>` works consistently inside and outside Docker.
"""
import os
import sys


def main() -> None:
    """Run Django management commands using this project's settings."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "auth_service.settings")

    # Import here so the settings module is configured before Django loads.
    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
