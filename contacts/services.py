import AddressBook as ab
from .models import Person, Address, ABPerson


def load_from_address_book():
    address_book = ab.ABAddressBook.sharedAddressBook()

    for raw_person in address_book.people():
        update_person(raw_person)

    address_book_ids = set(address_book.allUniqueIds())

    for person in Person.objects.all():
        if person.address_book_id not in address_book_ids:
            person.delete()


def update_person(raw_person):
    person, _ = Person.objects.get_or_create(address_book_id=raw_person.uniqueId())
    ab_person = ABPerson(raw_person)

    person.name = ab_person.name()
    person.organization = ab_person.organization()
    
    if person.name:
        person.save()

    update_addresses(person, ab_person)


def update_addresses(person, ab_person):
    addresses = set(person.address_set.all())
    ab_addresses = ab_person.ab_addresses()

    ab_addresses_elements = {ab_address.elements for ab_address in ab_addresses}
    for address in addresses:
        if address.elements not in ab_addresses_elements:
            address.delete()

    addresses_elements = {address.elements for address in addresses}
    for ab_address in ab_addresses:
        if ab_address.elements not in addresses_elements:
            person.create_address(ab_address)


def update_latlngs():
    for address in Address.objects.without_latlng():
        address.update_latlng()
