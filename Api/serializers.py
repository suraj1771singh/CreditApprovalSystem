from .models import Customer, Loan
from rest_framework import serializers
from .utils import loan_approval_status, calculate_interest_rate, calculate_credit_score, calculate_monthly_installment


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

    class Meta:
        model = Loan
        fields = ['loan_id', 'customer_id', 'loan_amount', 'interest_rate', 'tenure',
                  'monthly_installment', 'emis_paid_on_time', 'approval_date', 'end_date']
        extra_kwargs = {
            'approval_date': {'input_formats': ['%m/%d/%Y']},
            'end_date': {'input_formats': ['%m/%d/%Y']},
        }


class CustomerDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'first_name', 'last_name', 'phone_number', 'age']


class LoanDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Loan
        fields = ['id', 'loan_amount',
                  'interest_rate', 'monthly_installment', 'tenure']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        customer_id = instance.customer_id
        if customer_id is not None:
            customer_instance = Customer.objects.get(pk=customer_id)
            customer_serializer = CustomerDetailSerializer(customer_instance)
            representation['customer'] = customer_serializer.data
        return representation


class LoanListSerializer(serializers.ModelSerializer):
    repayments_left = serializers.IntegerField(
        source='get_repayments_left', read_only=True)

    class Meta:
        model = Loan
        fields = ['id', 'loan_amount',
                  'interest_rate', 'monthly_installment', 'repayments_left']
