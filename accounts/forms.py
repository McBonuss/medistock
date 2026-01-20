from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Organisation, Location

BOOTSTRAP_INPUT = {'class': 'form-control'}

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs=BOOTSTRAP_INPUT))
    organisation_name = forms.CharField(
        max_length=120,
        required=False,
        help_text='Optional: create your organisation',
        widget=forms.TextInput(attrs=BOOTSTRAP_INPUT),
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'organisation_name', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update(BOOTSTRAP_INPUT)
        self.fields['password1'].widget.attrs.update(BOOTSTRAP_INPUT)
        self.fields['password2'].widget.attrs.update(BOOTSTRAP_INPUT)

    def save(self, commit=True):
        user = super().save(commit=commit)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        org_name = self.cleaned_data.get('organisation_name')
        if org_name:
            org, _ = Organisation.objects.get_or_create(name=org_name)
            profile = user.profile
            profile.organisation = org
            profile.role = profile.ROLE_ORG_ADMIN
            profile.save()
            Location.objects.get_or_create(organisation=org, name='Main Location')
        return user

class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ['name', 'address_line1', 'city', 'postcode']
        widgets = {
            'name': forms.TextInput(attrs=BOOTSTRAP_INPUT),
            'address_line1': forms.TextInput(attrs=BOOTSTRAP_INPUT),
            'city': forms.TextInput(attrs=BOOTSTRAP_INPUT),
            'postcode': forms.TextInput(attrs=BOOTSTRAP_INPUT),
        }

    def clean_postcode(self):
        value = (self.cleaned_data.get('postcode') or '').strip()
        if value and len(value) < 3:
            raise forms.ValidationError('Postcode seems too short.')
        return value
