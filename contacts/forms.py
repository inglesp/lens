from django import forms

class SearchForm(forms.Form):
    postcode = forms.CharField(max_length=10)
    distance_in_miles = forms.IntegerField(initial=20)
