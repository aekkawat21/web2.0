from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import UserProfile, Item 


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2' )
        widgets = {
            'password1': forms.PasswordInput(),
            'password2': forms.PasswordInput(),
            'email':forms.EmailInput(),
        }

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['picture']

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['brand', 'model', 'color', 'category', 'serial_number','store_date_of_purchase', 'store_of_purchase', 'warranty', 'image', ]
        widgets = {
            'brand': forms.TextInput(attrs={'required': 'required'}),
            'model': forms.TextInput(attrs={'required': 'required'}), 
            'color': forms.TextInput(attrs={'required': 'required'}), 
            'category': forms.Select(attrs={'required': 'required'}), 
            'image': forms.FileInput(attrs={'required': 'required'}), 
            'serial_number': forms.TextInput(attrs={'required': 'required'}),
            'store_of_purchase': forms.TextInput(attrs={'required': 'required'}), 
            'warranty': forms.TextInput(attrs={'required': 'required'}),
            'store_date_of_purchase': forms.DateInput(format=('%Y-%m-%d'), attrs={'type': 'date', 'required': 'required'}),
            
        }
        labels={
            'brand': 'แบรนด์',
            'model': 'รุ่น', 
            'color': 'สี', 
            'category': 'หมวดหมู่', 
            'image': 'รูป', 
            'serial_number': 'เลขผลิตภัณฑ์',
            'store_of_purchase': 'ร้านที่ซื้อ', 
            'warranty': 'ประกัน',
            'store_date_of_purchase':'วันที่ซื้อ',
        }
   

class ItemEditForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = [
            'category', 'brand', 'model', 'color', 'serial_number', 'image',
            'store_date_of_purchase', 'warranty', 
        ]
        widgets = {
            'brand': forms.TextInput(),
            'model': forms.TextInput(), 
            'color': forms.TextInput(), 
            'category': forms.Select(),    
            'serial_number': forms.TextInput(),
            'store_of_purchase': forms.TextInput(), 
            'warranty': forms.TextInput(),
            'store_date_of_purchase': forms.DateInput(format=('%Y-%m-%d'), attrs={'type': 'date'}),
            'previous_owners': forms.CheckboxSelectMultiple(),
        }
        labels = {
            'category': 'หมวดหมู่',
            'brand': 'ยี่ห้อ',
            'model': 'รุ่น',
            'color': 'สี',
            'serial_number': 'หมายเลขซีเรียล',
            'image': 'รูปภาพ',
            'store_date_of_purchase': 'วันที่ซื้อ',
            'warranty': 'การรับประกัน',
            'previous_owners': 'ผู้ใช้คนก่อน'
        }
     
    def clean(self):
        cleaned_data = super().clean()
        current_owner = cleaned_data.get("current_owner")
        previous_owners = cleaned_data.get("previous_owners")
        if current_owner and previous_owners:
            if current_owner in previous_owners:
                self.add_error('current_owner', 'ผู้ใช้ปัจจุบันไม่สามารถอยู่ในรายการผู้ใช้คนก่อนได้.')
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
       
class EditPersonalDetailsForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['name', 'age', 'gender']
              
class TransferItemForm(forms.Form):
    new_owner_username = forms.CharField(label='ชื่อผู้ใช้ใหม่', max_length=150) 
    
   
  