from django.shortcuts import render
from rest_framework import generics
from .models import Customer, Loan
from .serializers import CustomerSerializer, LoanSerializer


class CustomerView(generics.ListCreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class LoanView(generics.ListCreateAPIView):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer
