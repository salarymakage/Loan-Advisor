from django.urls import path
from .views import dashboard_view, admin_dashboard_view, apply_loan_view, loan_detail_view


app_name = "dashboard"

urlpatterns = [
    path('', dashboard_view, name='dashboard'),
    path('admin/', admin_dashboard_view, name='admin_dashboard'),
    path('apply-loan/', apply_loan_view, name='apply_loan'),
    path('loan/<int:loan_id>/', loan_detail_view, name='loan_detail'),
    
]
