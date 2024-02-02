from django.shortcuts import get_object_or_404
from rest_framework import generics
from .models import Customer, Loan
from .serializers import CustomerSerializer, LoanSerializer, LoanDetailSerializer, LoanListSerializer
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


class LoanDetailView(generics.RetrieveAPIView):
    queryset = Loan.objects.all()

    def get_serializer_class(self):
        if 'loan_id' in self.request.query_params:
            return LoanDetailSerializer
        elif 'customer_id' in self.request.query_params:
            return LoanListSerializer
        else:
            return LoanSerializer

    def retrieve(self, request, *args, **kwargs):
        loan_id = request.query_params.get('loan_id')
        customer_id = request.query_params.get('customer_id')

        if loan_id:
            instance = Loan.objects.get(pk=loan_id)
            serializer_class = self.get_serializer_class()
            serializer = serializer_class(instance)
        elif customer_id:
            instance = Loan.objects.filter(customer_id=customer_id)
            serializer_class = self.get_serializer_class()
            serializer = serializer_class(instance, many=True)
        else:
            instance = Loan.objects.all()
            serializer_class = self.get_serializer_class()
            serializer = serializer_class(instance, many=True)

        return Response(serializer.data)


@api_view(['POST'])
def createLoan(request):
    if request.method == 'POST':

        customer_id = request.data.get('customer_id')
        loan_amount = request.data.get('loan_amount')
        tenure = request.data.get('tenure')

        # Check customer exits
        customer = get_object_or_404(Customer, pk=customer_id)

        try:
            credit_score = calculate_credit_score(customer_id, loan_amount)

            if loan_approval_status(customer_id, credit_score):
                interest_rate = calculate_interest_rate(credit_score)
                monthly_installment = calculate_monthly_installment(
                    loan_amount, interest_rate, tenure)
                serializer_data = {
                    'customer_id': customer_id,
                    'loan_amount': loan_amount,
                    'tenure': tenure,
                    'interest_rate': interest_rate,
                    'monthly_installment': monthly_installment,
                }
                serializer = LoanSerializer(
                    data=serializer_data)
                if serializer.is_valid():
                    loan = serializer.save()
                    res_data = {
                        'loan_id': loan.id,
                        'customer_id': loan.customer_id,
                        'loan_approved': True,
                        'monthly_installment': loan.monthly_installment
                    }
                    return Response(res_data, status=status.HTTP_201_CREATED)
            else:
                res_data = {
                    'loan_id': None,
                    'customer_id': customer_id,
                    'loan_approved': False,
                    'message': "Customer have Low Credit Score",
                    'monthly_installment': 0
                }
                return Response(res_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def check_eligibility(request):
    if request.method == 'POST':

        customer_id = request.data.get("customer_id")
        interest_rate = request.data.get("interest_rate")
        tenure = request.data.get("tenure")
        loan_amount = request.data.get("loan_amount")

        customer = get_object_or_404(Customer, pk=customer_id)

        # Check if required fields are present
        if not all([customer_id, interest_rate, tenure, loan_amount]):
            return Response({"error": "Missing required fields."}, status=status.HTTP_400_BAD_REQUEST)

        try:

            credit_score = calculate_credit_score(customer_id, loan_amount)

            if not loan_approval_status(customer_id, credit_score):
                return Response({"customer_id": customer_id, "approval": False}, status=status.HTTP_200_OK)

            new_interest_rate = calculate_interest_rate(credit_score)

            monthly_installment = calculate_monthly_installment(
                loan_amount, max(interest_rate, new_interest_rate), tenure)

            response_data = {
                "customer_id": customer_id,
                "approval": True,
                'interest_rate': interest_rate,
                "corrected_interest_rate": max(interest_rate, new_interest_rate),
                "tenure": tenure,
                "monthly_installment": monthly_installment
            }

            return Response(response_data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
