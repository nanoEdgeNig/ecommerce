from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError

class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        max_length=150,
        help_text="",
    )
    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput,
        help_text="",
    )
    password2 = forms.CharField(
        label="Password confirmation",
        widget=forms.PasswordInput,
        strip=False,
        help_text="", 
    )

    class Meta:
        model = User
        fields = ("username", "password1", "password2")

    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")
        try:
            return super().clean_password1()
        except ValidationError:
            raise ValidationError("Please enter a valid password.")
