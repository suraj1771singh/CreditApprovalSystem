from .models import Customer, Loan
from rest_framework import serializers


class CustomerSerializer(serializers.ModelSerializer):
    customer_id = serializers.IntegerField(
        source='get_customer_id', read_only=True)
    name = serializers.CharField(
        source='get_customer_full_name', read_only=True)

    class Meta:
        model = Customer
        fields = ['customer_id', 'name', 'first_name', 'last_name', 'age',
                  'monthly_income', 'approved_limit', 'phone_number']
        extra_kwargs = {
            'first_name': {'write_only': True},
            'last_name': {'write_only': True},
        }


class LoanSerializer(serializers.ModelSerializer):
    loan_id = serializers.IntegerField(
        source='get_loan_id', read_only=True)

    loan_approved = serializers.BooleanField(
        source='is_loan_approved', read_only=True)

    class Meta:
        model = Loan
        fields = ['loan_id', 'customer_id', 'get_loan_id', 'loan_amount', 'loan_approved', 'interest_rate', 'tenure',
                  'monthly_installment', 'emis_paid_on_time', 'approval_date', 'end_date']
        extra_kwargs = {
            'approval_date': {'input_formats': ['%m/%d/%Y']},
            'end_date': {'input_formats': ['%m/%d/%Y']},
        }
