from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib import messages
from .forms import SignUpForm
from .models import UserProfile, OTP
import requests

# Create your views here.

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            mobile_number = form.cleaned_data.get('mobile_number')
            otp = form.cleaned_data.get('otp')

            if not otp:
                # Generate and send OTP
                otp_code = OTP.generate_otp()
                OTP.objects.create(mobile_number=mobile_number, otp=otp_code)
                
                # Here you would typically send the OTP via SMS
                # For testing, we'll just show it
                messages.info(request, f'OTP sent to {mobile_number}: {otp_code}')
                return render(request, 'accounts/signup.html', {'form': form, 'otp_sent': True})
            
            # Verify OTP
            try:
                otp_obj = OTP.objects.get(mobile_number=mobile_number, otp=otp, is_verified=False)
                otp_obj.is_verified = True
                otp_obj.save()

                user = form.save()
                UserProfile.objects.create(user=user, mobile_number=mobile_number, is_mobile_verified=True)
                login(request, user)
                messages.success(request, 'Account created successfully!')
                return redirect('home')
            except OTP.DoesNotExist:
                messages.error(request, 'Invalid OTP')
                return render(request, 'accounts/signup.html', {'form': form, 'otp_sent': True})
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('home')
