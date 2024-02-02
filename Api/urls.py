from django.urls import path, include
from .views import CustomerView, LoanView, check_eligibility, LoanDetailView


urlpatterns = [
    path('register/', CustomerView.as_view(), name='register-customer'),
    path('create-loan/', LoanView.as_view(), name='create-loan'),
    path('check-eligibility/', check_eligibility, name='check-eligibility'),
    path('view-loan/', LoanDetailView.as_view(), name='loan-detail'),
]
