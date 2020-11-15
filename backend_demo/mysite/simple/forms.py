from django import forms

class JSONForm(forms.Form):
    json = forms.CharField(label='JSON: ', max_length=100)
