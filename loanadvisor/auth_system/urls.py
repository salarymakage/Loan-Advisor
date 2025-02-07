from django.urls import path
from .views import intro_view,signup_view, login_view, logout_view, otp_verification_view, forgot_password_view, verify_otp_view, reset_password_view
from django.conf import settings
from django.conf.urls.static import static
app_name = "auth_system"

urlpatterns = [
    path('', intro_view, name='intro'),
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('otp-verification/', otp_verification_view, name='otp_verification'),
    
    path('forgot-password/', forgot_password_view, name='forgot_password'),
    path('verify-otp/', verify_otp_view, name='verify_otp'),
    path('reset-password/', reset_password_view, name='reset_password'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
