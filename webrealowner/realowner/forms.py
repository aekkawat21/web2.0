from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import UserProfile, Item 



class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['picture']


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['brand', 'model', 'color', 'category', 'image', 'serial_number','store_date_of_purchase', 'store_of_purchase', 'warranty', ]
        widgets = {
            'store_date_of_purchase': forms.DateInput(format=('%Y-%m-%d'), attrs={'type': 'date'}),
        }

class ItemEditForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = [
            'category', 'brand', 'model', 'color', 'serial_number', 'image',
            'store_date_of_purchase', 'warranty', 'description', 'current_owner', 'previous_owners'
        ]
        widgets = {
            'store_date_of_purchase': forms.DateInput(attrs={'type': 'date'}),
            'previous_owners': forms.CheckboxSelectMultiple,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['current_owner'].queryset = UserProfile.objects.all()
        self.fields['previous_owners'].queryset = UserProfile.objects.all()

    def clean(self):
        cleaned_data = super().clean()
        current_owner = cleaned_data.get("current_owner")
        previous_owners = cleaned_data.get("previous_owners")
        if current_owner in previous_owners:
            self.add_error('current_owner', 'Current owner cannot be in the list of previous owners.')
        return cleaned_data

class EmailUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True, help_text='Enter a new email address')

    class Meta:
        model = User
        fields = ('email',)

class ContactChannelsForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone_number', ]

class f(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['name','age','gender', ]        


class TransferItemForm(forms.Form):
    item_serial_number = forms.CharField(label='Item Serial Number', max_length=255)
    new_owner_username = forms.CharField(label='New Owner Username', max_length=150)        