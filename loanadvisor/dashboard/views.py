from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect
from .forms import LoanApplicationForm
from .models import LoanApplication
from joblib import load
import pandas as pd
from .forms import AdminUserForm
from django.contrib.auth.models import User
import os 
from django.shortcuts import render, get_object_or_404


MODEL_PATH = os.path.join(os.path.dirname(__file__), 'models')

# Load saved pipelines
risk_pipeline = load(os.path.join(MODEL_PATH, "risk_prediction_pipeline.joblib"))
loan_pipeline = load(os.path.join(MODEL_PATH, "loan_approval_pipeline.joblib"))


@login_required
def dashboard_view(request):
    user = request.user

    # Retrieve the phone number from the CustomUser model
    phone_number = user.phone_number if hasattr(user, 'phone_number') else None

    # Alternatively, check the Profile model if the phone number is stored there
    if not phone_number and hasattr(user, 'profile'):
        phone_number = user.profile.phone_number

    # Retrieve loan applications for the logged-in user
    loans = user.loan_applications.all()

    context = {
        'name': user.username,
        'phone_number': phone_number if phone_number else "N/A",
        'loans': loans,
    }
    return render(request, 'dashboard/dashboard.html', context)




@login_required
@user_passes_test(lambda u: u.is_staff)
def admin_dashboard_view(request):
    if request.method == "POST":
        form = AdminUserForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, "dashboard/admin_dashboard.html", {"form": form, "success": "User created successfully!"})
    else:
        form = AdminUserForm()

    return render(request, "dashboard/admin_dashboard.html", {"form": form})


@login_required
def apply_loan_view(request):
    if request.method == "POST":
        form = LoanApplicationForm(request.POST)
        if form.is_valid():
            # Get the cleaned data
            data = form.cleaned_data

            # Prepare the sample for prediction
            sample = pd.DataFrame({
                "Province": [data['province']],
                "Region Type": [data['region_type']],
                "Age": [data['age']],
                "Gender": [data['gender']],
                "Employment Type": [data['employment_type']],
                "Annual Income (USD)": [data['annual_income']],
                "Credit History": [data['credit_history']],
                "Existing Debt (USD)": [data['existing_debt']],
                "Savings/Assets (USD)": [data['savings_assets']],
                "Loan Type": [data['loan_type']],
                "Loan Amount (USD)": [data['loan_amount']],
                "Loan Term (Years)": [data['loan_term_years']],
                "Annual Interest Rate (%)": [data['annual_interest_rate']],
                "Collateral (USD)": [data['collateral']],
            })

            # Perform prediction
            risk_pred = risk_pipeline.predict(sample)[0]
            loan_status = loan_pipeline.predict(sample)[0]
            loan_status_text = "Approved" if loan_status == 1 else "Rejected"

            # Save the loan application details to the database
            LoanApplication.objects.create(
                user=request.user,
                province=data['province'],
                region_type=data['region_type'],
                age=data['age'],
                gender=data['gender'],
                employment_type=data['employment_type'],
                annual_income=data['annual_income'],
                credit_history=data['credit_history'],
                existing_debt=data['existing_debt'],
                savings_assets=data['savings_assets'],
                loan_type=data['loan_type'],
                loan_amount=data['loan_amount'],
                loan_term_years=data['loan_term_years'],
                annual_interest_rate=data['annual_interest_rate'],
                collateral=data['collateral'],
                risk_prediction=risk_pred,
                loan_status=loan_status_text,
            )

            # Redirect to the dashboard
            return redirect('dashboard:dashboard')
    else:
        form = LoanApplicationForm()

    return render(request, 'dashboard/apply_loan.html', {'form': form})

@login_required
def loan_detail_view(request, loan_id):
    loan = get_object_or_404(LoanApplication, id=loan_id, user=request.user)
    return render(request, 'dashboard/loan_detail.html', {'loan': loan})