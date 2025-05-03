from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile, OTP

class SignUpForm(UserCreationForm):
    mobile_number = forms.CharField(max_length=15, required=True)
    otp = forms.CharField(max_length=6, required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'mobile_number', 'otp')

    def clean_mobile_number(self):
        mobile_number = self.cleaned_data.get('mobile_number')
        if UserProfile.objects.filter(mobile_number=mobile_number).exists():
            raise forms.ValidationError("This mobile number is already registered.")
        return mobile_number 