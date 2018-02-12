"""Management command to easily create test data."""
from app.events.factories import EventFactory
from app.events.models import Event

from django.core.management.base import BaseCommand
from django.db.models import Max


class Command(BaseCommand):  # noqa: D101
    help = 'Creates test event data.'

    def add_arguments(self, parser):  # noqa: D102
        # Positional arguments
        parser.add_argument('number_of_events', type=int)

        # parser.add_argument(
        #     '--past',
        #     action='store_true',
        #     dest='past',
        #     help='Create past events.',
        # )

        # parser.add_argument(
        #     '--future',
        #     action='store_true',
        #     dest='future',
        #     help='Create events in the far future (think > 1year).',
        # )

    def handle(self, *args, **options):  # noqa: D102
        num = options['number_of_events']

        EventFactory.create_batch(num)

        self.stdout.write(self.style.SUCCESS('Successfully created {} new events.'.format(num)))
