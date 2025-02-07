from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from dashboard.models import LoanApplication
from .models import CustomUser, UserToken, Profile
from django.utils.html import format_html


class LoanApplicationInline(admin.TabularInline):
    model = LoanApplication
    extra = 0
    fields = ('loan_type', 'loan_amount', 'loan_status', 'risk_prediction', 'created_at', 'action_buttons')
    readonly_fields = ('loan_type', 'loan_amount', 'risk_prediction', 'created_at', 'action_buttons')
    can_delete = False

    def action_buttons(self, obj):
        """Provide buttons to accept or reject a loan."""
        if obj.loan_status == 'Pending':
            return format_html(
                '<a class="button" style="margin-right: 5px;" href="/admin/dashboard/loanapplication/{}/approve/">Approve</a>'
                '<a class="button" style="background-color: red; color: white;" href="/admin/dashboard/loanapplication/{}/reject/">Reject</a>',
                obj.id,
                obj.id,
            )
        return "No action required"

    action_buttons.short_description = 'Actions'
    action_buttons.allow_tags = True


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    inlines = [LoanApplicationInline]  # Include LoanApplicationInline
    list_display = ('username', 'email', 'phone_number', 'is_staff', 'is_superuser', 'is_approved')
    list_filter = ('is_staff', 'is_superuser', 'is_approved')
    search_fields = ('username', 'email', 'phone_number')

    fieldsets = (
        ("Personal Info", {
            'fields': ('username', 'email', 'phone_number', 'password')
        }),
        ("Permissions", {
            'fields': ('is_staff', 'is_superuser', 'is_active', 'groups', 'user_permissions'),
        }),
        ("Status", {
            'fields': ('is_approved',),
        }),
        ("Important Dates", {
            'fields': ('last_login', 'date_joined'),
        }),
    )

    # Admin actions
    actions = ['approve_users', 'reject_users']

    @admin.action(description='Approve selected users')
    def approve_users(self, request, queryset):
        queryset.update(is_approved=True)
        self.message_user(request, "Selected users have been approved.")

    @admin.action(description='Reject selected users')
    def reject_users(self, request, queryset):
        queryset.update(is_approved=False)
        self.message_user(request, "Selected users have been rejected.")


from django.contrib import admin
from dashboard.models import LoanApplication
from auth_system.models import CustomUser, Profile


@admin.register(LoanApplication)
class LoanApplicationAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'loan_type', 'loan_amount', 'loan_status', 'risk_prediction', 'created_at')
    list_filter = ('loan_status', 'risk_prediction')
    search_fields = ('user__username', 'loan_type', 'loan_amount')

    def phone_number(self, obj):
        """Retrieve the phone number from the related CustomUser model."""
        return obj.user.phone_number if hasattr(obj.user, 'phone_number') else "N/A"

    phone_number.short_description = 'Phone Number'

    # Define actions for Approve, Reject, and Set Risk Levels
    actions = ['approve_selected_loans', 'reject_selected_loans', 'set_low_risk', 'set_medium_risk', 'set_high_risk']

    @admin.action(description='Approve selected loans')
    def approve_selected_loans(self, request, queryset):
        queryset.update(loan_status='Approved')
        self.message_user(request, f"{queryset.count()} loan(s) approved successfully.")

    @admin.action(description='Reject selected loans')
    def reject_selected_loans(self, request, queryset):
        queryset.update(loan_status='Rejected')
        self.message_user(request, f"{queryset.count()} loan(s) rejected successfully.")

    @admin.action(description='Set selected loans to Low Risk')
    def set_low_risk(self, request, queryset):
        queryset.update(risk_prediction='Low Risk')
        self.message_user(request, f"Risk prediction set to Low for {queryset.count()} loan(s).")

    @admin.action(description='Set selected loans to Medium Risk')
    def set_medium_risk(self, request, queryset):
        queryset.update(risk_prediction='Medium Risk')
        self.message_user(request, f"Risk prediction set to Medium for {queryset.count()} loan(s).")

    @admin.action(description='Set selected loans to High Risk')
    def set_high_risk(self, request, queryset):
        queryset.update(risk_prediction='High Risk')
        self.message_user(request, f"Risk prediction set to High for {queryset.count()} loan(s).")
