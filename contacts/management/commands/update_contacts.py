from django.core.management.base import BaseCommand

from contacts import services
from contacts.exceptions import OverQueryLimitError

class Command(BaseCommand):
    args = '[--latlngs-only]'
    help = '''
Update contacts data from local address book, and try to find
latitude/longitude via Google geocoding API.

Skip loading data from address book with --latlngs-only.
'''.strip()

    def handle(self, *args, **kwargs):
        print 'Updating data'

        if '--latlngs-only' not in args:
            print 'Loading contacts from address book'
            services.load_from_address_book()

        print 'Looking up latitudes and longitudes'

        try:
            services.update_latlngs()
            print 'Done'
        except OverQueryLimitError:
            print 'We have been rate-limited by Google -- please try agian later'

