from django import forms
from django.core.exceptions import ValidationError
from .models import CustomUser

class CustomUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['email', 'name', 'age', 'national_id_card_no']

   

    # Ensure all required fields are provided and valid
    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        name = cleaned_data.get('name')
        age = self.cleaned_data.get('age')
        national_id_card_no = cleaned_data.get('national_id_card_no')
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")


        if not password1 or not password2:
            raise ValidationError("Both password fields are required.")
        if age < 18:
            raise ValidationError("You must be at least 18 years old.")
        if not age:
            raise ValidationError(" Age is required.")
        if password1 != password2:
            raise ValidationError("Passwords do not match.")
        if not email:
            raise ValidationError("Email is required.")
        if not name:
            raise ValidationError("Name is required.")
        if not national_id_card_no:
            raise ValidationError("National ID Card Number is required.")

        return cleaned_data

    # Override the save method to set the password correctly
    def save(self, commit=False):
        user = super().save(commit=False)  # Don't save to the database yet

        return user  # Return the user without saving it yet


