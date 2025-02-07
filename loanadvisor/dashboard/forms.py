from django import forms
from django.contrib.auth.models import User
from auth_system.models import Profile

class AdminUserForm(forms.ModelForm):
    role = forms.ChoiceField(choices=Profile.ROLE_CHOICES, label="Role")

    class Meta:
        model = User
        fields = ['username', 'email', 'is_active', 'role']  # Include `role` field

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            # Update or create the profile
            Profile.objects.update_or_create(user=user, defaults={'role': self.cleaned_data['role']})
        return user

class LoanApplicationForm(forms.Form):
    province = forms.ChoiceField(choices=[("Phnom Penh", "Phnom Penh"), ("Kandal", "Kandal"), ("Siem Reap", "Siem Reap"), ("Svay Rieng", "Svay Rieng"), ("Kampong Speu", "Kampong Speu"), ("Kampong Thom", "Kampong Thom"), ("Battambang", "Battambang"), ("Other", "Other")])
    region_type = forms.ChoiceField(choices=[('Urban', 'Urban'), ('Semi-Urban', 'Semi-Urban'), ('Rural', 'Rural')])
    age = forms.IntegerField(min_value=18, max_value=100)
    gender = forms.ChoiceField(choices=[('Male', 'Male'), ('Female', 'Female')])
    employment_type = forms.ChoiceField(choices=[("Salaried", "Salaried"), ("Self-Employed", "Self-Employed"), ("Farmer", "Farmer"), ("Student", "Student"), ("Unemployed", "Unemployed")])
    annual_income = forms.FloatField()
    credit_history = forms.ChoiceField(choices=[("Good", "Good"), ("Fair", "Fair"), ("Poor", "Poor"), ("No History", "No History")])
    existing_debt = forms.FloatField()
    savings_assets = forms.FloatField()
    loan_type = forms.ChoiceField(choices=[("House", "House"), ("Agriculture", "Agriculture"), ("SME", "SME"), ("Moto", "Moto"), ("Car", "Car"), ("Personal", "Personal")])
    loan_amount = forms.FloatField()
    loan_term_years = forms.IntegerField()
    annual_interest_rate = forms.FloatField()
    collateral = forms.FloatField()
