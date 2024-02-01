import datetime
from django.db import models
from dateutil.relativedelta import relativedelta


class Customer(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    age = models.IntegerField()
    phone_number = models.BigIntegerField()
    monthly_income = models.IntegerField()
    approved_limit = models.IntegerField(blank=True, null=True)

    def get_customer_id(self):
        return self.id

    def get_customer_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def save(self, *args, **kwargs):

        # ---Calculate approved_limit
        if self.approved_limit is None:
            self.approved_limit = round(36 * self.monthly_income, -5)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.id}"


class Loan(models.Model):
    customer_id = models.IntegerField()
    loan_amount = models.FloatField()
    interest_rate = models.FloatField()
    tenure = models.IntegerField()
    monthly_installment = models.FloatField(blank=True, null=True)
    emis_paid_on_time = models.IntegerField(blank=True, null=True)
    approval_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)

    def get_loan_id(self):
        return self.id

    def is_loan_approved(self):
        return False

    def save(self, *args, **kwargs):

        # ---Checking if customer exist
        if not Customer.objects.filter(pk=self.customer_id).exists():
            raise ValueError(
                f"Customer with ID {self.customer_id} does not exist.")

        # ---Calculate end_date
        if not self.end_date:
            self.end_date = self.approval_date + \
                relativedelta(months=+self.tenure)

        # ---Calculate monthly installments
        if not self.monthly_installment:
            # logic to calculate monthly_payment
            self.monthly_installment = 80
        super().save(*args, **kwargs)
