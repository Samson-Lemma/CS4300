"""Configure Django for Behave tests."""

import os

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "movie_theater_booking.settings",
)

import django

django.setup()

from django.core.management import call_command
from django.test.runner import DiscoverRunner


def before_all(context):
    """Create an isolated Django test database for Behave."""
    context.test_runner = DiscoverRunner(
        verbosity=0,
        interactive=False,
    )

    context.test_runner.setup_test_environment()

    context.old_database_config = (
        context.test_runner.setup_databases()
    )


def before_scenario(context, scenario):
    """Clear test data before each Behave scenario."""
    call_command(
        "flush",
        verbosity=0,
        interactive=False,
    )


def after_all(context):
    """Destroy the Behave test database."""
    context.test_runner.teardown_databases(
        context.old_database_config
    )

    context.test_runner.teardown_test_environment()