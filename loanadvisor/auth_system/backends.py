from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model

User = get_user_model()

class PhoneNumberBackend(BaseBackend):
    """
    Custom authentication backend to authenticate users using phone number and password.
    """
    def authenticate(self, request, phone_number=None, password=None, **kwargs):
        try:
            # Get the user with the given phone number
            user = User.objects.get(phone_number=phone_number)
            # Check the user's password
            if user.check_password(password):
                user.backend = 'auth_system.backends.PhoneNumberBackend'
                return user
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
