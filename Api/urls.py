from django.urls import path
from .views import CustomerView, createLoan, check_eligibility, LoanDetailView


urlpatterns = [
    path('register/', CustomerView.as_view(), name='register-customer'),
    path('create-loan/', createLoan, name='create-loan'),
    path('check-eligibility/', check_eligibility, name='check-eligibility'),
    path('view-loan/', LoanDetailView.as_view(), name='loan-detail'),
]
