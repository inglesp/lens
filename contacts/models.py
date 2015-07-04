from django.db import models
from django.db.models import Q
from haversine import haversine

from . import utils

ADDRESS_FIELDS = ['Street', 'City', 'State', 'ZIP', 'Country']

class AddressesManager(models.Manager):
    def get_queryset(self):
        return super(AddressesManager, self).get_queryset().select_related('person')

    def with_latlng(self):
        return self.filter(~Q(lat='') & ~Q(lng=''))

    def without_latlng(self):
        return self.filter(Q(lat='') | Q(lng='')).exclude(latlng_error__in=['Multiple results returned', 'No results returned'])

    def near_to(self, latlng, radius_in_miles):
        print '-' * 80
        print 'Finding addresses within {} miles of {}'.format(radius_in_miles, latlng)
        addresses = []
        for address in self.with_latlng():
            print 'Considering: {} ({})'.format(address, address.person)
            distance_in_miles = haversine(address.latlng(), latlng, miles=True)
            print 'Distance in miles:', distance_in_miles
            if distance_in_miles < radius_in_miles:
                print 'Within distance'
                address.distance_in_miles = distance_in_miles
                addresses.append(address)

        print '-' * 80
        return sorted(addresses, key=lambda address: address.distance_in_miles)


class PersonManager(models.Manager):
    def get_queryset(self):
        return super(PersonManager, self).get_queryset().select_related('address_set')


class Person(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    address_book_id = models.CharField(max_length=255)

    objects = PersonManager()

    def __unicode__(self):
        return self.name

    def create_address(self, ab_address):
        attrs = dict(zip(ADDRESS_FIELDS, ab_address.elements))
        self.address_set.create(**attrs)


class Address(models.Model):
    person = models.ForeignKey(Person)
    Street = models.CharField(max_length=255)
    City = models.CharField(max_length=255)
    State = models.CharField(max_length=255)
    ZIP = models.CharField(max_length=255)
    Country = models.CharField(max_length=255)
    lat = models.CharField(max_length=255)
    lng = models.CharField(max_length=255)
    latlng_error = models.CharField(max_length=255)

    objects = AddressesManager()

    def __unicode__(self):
        return ', '.join(e for e in self.elements if e)

    @property
    def elements(self):
        return tuple(getattr(self, field) for field in ADDRESS_FIELDS)

    def update_latlng(self):
        try:
            self.lat, self.lng = utils.get_latlng(self.elements)
            self.latlng_error = ''
        except utils.LatLngError as e:
            self.lat, self.lng = '', ''
            print 'Error when updating latlng for {} ({})'.format(self, e)
            self.latlng_error = str(e)
        self.save()

    def latlng(self):
        return float(self.lat), float(self.lng)


class ABPerson(object):
    def __init__(self, raw_person):
        self.raw_person = raw_person

    def name(self):
        first = self.raw_person.valueForProperty_('First')
        last = self.raw_person.valueForProperty_('Last')

        if first is None and last is None:
            return None
        elif first is None:
            return last
        elif last is None:
            return first
        else:
            return u'{} {}'.format(first, last)

    def ab_addresses(self):
        address_prop = self.raw_person.valueForProperty_('Address')
        addresses = set()

        if address_prop is None:
            return set()
        else:
            ixs = range(address_prop.count())
            return {ABAddress(address_prop.valueAtIndex_(ix)) for ix in ixs}


class ABAddress(object):
    def __init__(self, address_dict):
        self.elements = tuple(address_dict.get(field, '') for field in ADDRESS_FIELDS)
