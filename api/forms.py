from django import forms
from .models import SafetyObject


class SafetyObjectForm(forms.ModelForm):
    class Meta:
        model = SafetyObject
        exclude = ['lokacija']
