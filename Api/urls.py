from django.urls import path, include
from .views import CustomerView, LoanView


urlpatterns = [
    path('register/', CustomerView.as_view()),
    path('create-loan/', LoanView.as_view()),
]
