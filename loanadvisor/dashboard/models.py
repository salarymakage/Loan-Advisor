from django.db import models
from django.contrib.auth.models import User
from django.conf import settings 

class LoanApplication(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='loan_applications')
    province = models.CharField(max_length=100)
    region_type = models.CharField(max_length=50)
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    employment_type = models.CharField(max_length=50)
    annual_income = models.FloatField()
    credit_history = models.CharField(max_length=50)
    existing_debt = models.FloatField()
    savings_assets = models.FloatField()
    loan_type = models.CharField(max_length=50)
    loan_amount = models.FloatField()
    loan_term_years = models.IntegerField()
    annual_interest_rate = models.FloatField()
    collateral = models.FloatField()
    risk_prediction = models.CharField(max_length=50)
    loan_status = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Loan Application ({self.loan_type}) - {self.user.username}"