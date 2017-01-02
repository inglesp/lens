from django.shortcuts import render

from .forms import SearchForm
from .models import Address, Person
from .utils import get_latlng

def all(request):
    context = {
        'people': Person.objects.order_by('name'),
        'form': SearchForm()
    }
    return render(request, 'contacts/all.html', context)

def with_errors(request):
    context = {
        'people': Person.objects.exclude(address__isnull=True).exclude(address__latlng_error='').order_by('name'),
        'form': SearchForm()
    }
    return render(request, 'contacts/all.html', context)

def with_addresses(request):
    context = {
        'people': Person.objects.exclude(address__isnull=True).order_by('name'),
        'form': SearchForm()
    }
    return render(request, 'contacts/all.html', context)

def without_addresses(request):
    context = {
        'people': Person.objects.exclude(address__isnull=False).order_by('name'),
        'form': SearchForm()
    }
    return render(request, 'contacts/all.html', context)

def search(request):
    postcode = request.GET.get('postcode')
    if postcode:
        lat, lng = get_latlng([postcode])

        try:
            distance = int(request.GET['distance_in_miles'])
        except ValueError:
            distance = 20

        form = SearchForm(request.GET)

        if lat is not None and lng is not None:
            nearby_addresses = Address.objects.near_to((lat, lng), distance)
            context = {'form': form, 'addresses': nearby_addresses}
            return render(request, 'contacts/search.html', context)

    form = SearchForm()
    context = {'form': form, 'addresses': None}
    return render(request, 'contacts/search.html', context)
