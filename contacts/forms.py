from django import forms

class SearchForm(forms.Form):
    distance_in_miles = forms.IntegerField(initial=20)
    postcode = forms.CharField(initial="SG8 7DP")
