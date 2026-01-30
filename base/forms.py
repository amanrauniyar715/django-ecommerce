from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
import re
from .models import Order
class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')

        # Check for uniqueness
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email is already registered.")

        # Only allow Gmail addresses (optional)
        if not email.endswith('@gmail.com'):
            raise ValidationError("Email must end with '@gmail.com'")

        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')

        # Reject if username is only digits
        if username.isdigit():
            raise ValidationError("Username cannot consist of only numbers.")

        # Require at least one alphabet character
        if not re.search(r'[a-zA-Z]', username):
            raise ValidationError("Username must contain at least one letter.")

        # Optional: enforce minimum length
        if len(username) < 4:
            raise ValidationError("Username must be at least 4 characters long.")

        return username



class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = '__all__'
