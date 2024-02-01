from django.shortcuts import render
from rest_framework import generics
from .models import Customer, Loan
from .serializers import CustomerSerializer, LoanSerializer
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from .utils import calculate_credit_score, calculate_interest_rate, loan_approval_status, calculate_monthly_installment


class CustomerView(generics.ListCreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class LoanView(generics.ListCreateAPIView):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer


@api_view(['POST'])
def check_eligibility(request):
    if request.method == 'POST':
        try:
            customer_id = request.data.get("customer_id")
            interest_rate = request.data.get("interest_rate")
            tenure = request.data.get("tenure")
            loan_amount = request.data.get("loan_amount")

            # Check if required fields are present
            if not all([customer_id, interest_rate, tenure, loan_amount]):
                return Response({"error": "Missing required fields."}, status=status.HTTP_400_BAD_REQUEST)

            credit_score = calculate_credit_score(customer_id)

            if not loan_approval_status(customer_id, credit_score):
                return Response({"customer_id": customer_id, "approval": False}, status=status.HTTP_200_OK)

            new_interest_rate = calculate_interest_rate(credit_score)

            if interest_rate < new_interest_rate:
                monthly_installment = calculate_monthly_installment(
                    loan_amount, new_interest_rate, tenure)
            else:
                monthly_installment = calculate_monthly_installment(
                    loan_amount, interest_rate, tenure)

            response_data = {
                "customer_id": customer_id,
                "approval": True,
                'interest_rate': interest_rate,
                "corrected_interest_rate": new_interest_rate,
                "tenure": tenure,
                "monthly_installment": monthly_installment
            }

            return Response(response_data, status=status.HTTP_200_OK)

        except Exception as e:
            # Log or handle the exception according to your application's needs
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
