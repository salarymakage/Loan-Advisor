from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.crypto import get_random_string
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
from .models import UserToken, CustomUser, Profile

# Import the Custom User model
User = get_user_model()

# View: Intro page
def intro_view(request):
    return render(request, 'auth_system/intro.html')

# Helper: Generate tokens for a user
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    tokens = {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
    # Save tokens in the database
    UserToken.objects.update_or_create(
        user=user,
        defaults={
            'access_token': tokens['access'],
            'refresh_token': tokens['refresh'],
        }
    )
    return tokens

# View: Signup
def signup_view(request):
    if request.method == "POST":
        name = request.POST.get("name")
        phone_number = request.POST.get("phone_number")
        password = request.POST.get("password")
        re_password = request.POST.get("re_password")

        # Validate inputs
        if not name or not phone_number or not password or not re_password:
            return render(request, 'auth_system/signup.html', {"error": "All fields are required."})

        if password != re_password:
            return render(request, 'auth_system/signup.html', {"error": "Passwords do not match."})

        if CustomUser.objects.filter(phone_number=phone_number).exists():
            return render(request, 'auth_system/signup.html', {"error": "Phone number already exists."})

        # Temporarily store data in session
        request.session['signup_data'] = {
            'name': name,
            'phone_number': phone_number,
            'password': password,
        }

        # Redirect to OTP verification
        return redirect('auth_system:otp_verification')

    return render(request, "auth_system/signup.html")




from django.contrib.auth import login

from django.contrib.auth import login

def otp_verification_view(request):
    if request.method == "POST":
        otp = request.POST.get("otp")
        if otp == "123456":  # Simple OTP check
            signup_data = request.session.get('signup_data')
            if not signup_data:
                return redirect('auth_system:signup')

            # Create the user
            user = CustomUser.objects.create_user(
                username=signup_data['name'],
                phone_number=signup_data['phone_number'],
                password=signup_data['password']
            )

            # Generate tokens for the user
            tokens = get_tokens_for_user(user)

            # Print tokens for debugging purposes
            print(f"Access Token for {user.username}: {tokens['access']}")
            print(f"Refresh Token for {user.username}: {tokens['refresh']}")

            # Log in the user
            login(request, user, backend='auth_system.backends.PhoneNumberBackend')

            # Redirect to dashboard
            return redirect("dashboard:dashboard")
        else:
            return render(request, 'auth_system/otp_verification.html', {"error": "Invalid OTP."})

    return render(request, 'auth_system/otp_verification.html')

from django.contrib.auth import login

def login_view(request):
    if request.method == "POST":
        phone_number = request.POST.get("phone_number")
        password = request.POST.get("password")

        # Authenticate using phone number
        user = authenticate(request, phone_number=phone_number, password=password)

        if user is not None:
            # Explicitly set the backend for the authenticated user
            login(request, user, backend=user.backend)

            # Generate tokens for the user
            tokens = get_tokens_for_user(user)

            # Print tokens to the console for debugging purposes
            print(f"Access Token for {user.username}: {tokens['access']}")
            print(f"Refresh Token for {user.username}: {tokens['refresh']}")

            # Redirect based on role
            if hasattr(user, 'profile') and user.profile.role == 'admin':
                return redirect("dashboard:admin_dashboard")
            else:
                return redirect("dashboard:dashboard")

        return render(request, "auth_system/login.html", {"error": "Invalid phone number or password."})
    return render(request, "auth_system/login.html")


# View: Forgot Password

def forgot_password_view(request):
    if request.method == "POST":
        phone_number = request.POST.get("phone_number")

        try:
            # Query the CustomUser model for the phone number
            user = User.objects.get(phone_number=phone_number)
        except User.DoesNotExist:
            return render(request, "auth_system/forgot_password.html", {"error": "Phone number not found."})

        # Store the phone number in the session for password reset
        request.session['phone_number'] = phone_number
        return redirect("auth_system:verify_otp")

    return render(request, "auth_system/forgot_password.html")


# View: Verify OTP for Password Reset
def verify_otp_view(request):
    if request.method == "POST":
        otp = request.POST.get("otp")
        if otp == "123456":  # Replace this with your OTP generation logic
            return redirect("auth_system:reset_password")
        return render(request, "auth_system/verify_otp.html", {"error": "Invalid OTP."})
    return render(request, "auth_system/verify_otp.html")


# View: Reset Password
def reset_password_view(request):
    phone_number = request.session.get('phone_number')
    if not phone_number:
        return redirect("auth_system:forgot_password")

    if request.method == "POST":
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")
        if new_password != confirm_password:
            return render(request, "auth_system/reset_password.html", {"error": "Passwords do not match."})

        try:
            # Retrieve the user directly from the `CustomUser` model using `phone_number`
            user = User.objects.get(phone_number=phone_number)
            user.set_password(new_password)  # Set the new password
            user.save()  # Save the updated user instance

            # Clear the session and redirect to the login page
            request.session.flush()
            return redirect("auth_system:login")
        except User.DoesNotExist:
            return redirect("auth_system:forgot_password")

    return render(request, "auth_system/reset_password.html")

# View: Logout
def logout_view(request):
    logout(request)
    return redirect("auth_system:intro")
