from django import forms
from django.forms.forms import Form


class CreateNewList(forms.Form):
    name = forms.CharField(label='name',max_length=200)
    check = forms.BooleanField(required=False)
