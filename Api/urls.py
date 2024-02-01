from django.urls import path, include
from .views import CustomerView, LoanView, check_eligibility


urlpatterns = [
    path('register/', CustomerView.as_view()),
    path('create-loan/', LoanView.as_view()),
    path('check-eligibility/', check_eligibility),
]
