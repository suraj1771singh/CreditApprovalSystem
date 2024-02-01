import logging
from .models import Customer, Loan
from django.db.models import Sum, Min
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
import math

logger = logging.getLogger(__name__)


def calculate_credit_score(customer_id):
    try:
        score = (
            0.4 * calculate_past_loan_paid_on_time_score(customer_id)
            + 0.2 * calculate_loan_taken_in_past_score(customer_id)
            + 0.2 * calculate_loan_activity_current_year_score(customer_id)
            + 0.2 * calculate_loan_approved_volume_score(customer_id)
        )

        return math.ceil(score)
    except Exception as e:
        logger.error(
            f"Error calculating credit score for customer {customer_id}: {e}")


def calculate_past_loan_paid_on_time_score(customer_id):
    try:
        count_paid_emis = Loan.objects.filter(customer_id=customer_id).aggregate(
            Sum("emis_paid_on_time")
        )["emis_paid_on_time__sum"]
        count_total_emis = Loan.objects.filter(customer_id=customer_id).aggregate(
            Sum("tenure")
        )["tenure__sum"]

        if count_total_emis and count_total_emis != 0:
            return round((count_paid_emis / count_total_emis) * 100, 2)
        else:
            return 0.0
    except Exception as e:
        logger.error(
            f"Error calculating past loan paid on time score for customer {customer_id}: {e}"
        )


def calculate_loan_taken_in_past_score(customer_id):
    try:
        count_loans = get_count_of_loans(customer_id)

        if count_loans:
            return round(1 / (1 + count_loans) * 100, 2)
        else:
            return 0.0
    except Exception as e:
        logger.error(
            f"Error calculating loan taken in past score for customer {customer_id}: {e}"
        )


def calculate_loan_activity_current_year_score(customer_id):
    try:
        current_year = timezone.now().year
        count_current_year_loans = Loan.objects.filter(
            customer_id=customer_id, approval_date__year=current_year
        ).count()
        count_total_loans = get_count_of_loans(customer_id)

        if count_total_loans:
            return round(count_current_year_loans / count_total_loans * 100, 2)
        else:
            return 0.0
    except Exception as e:
        logger.error(
            f"Error calculating loan activity current year score for customer {customer_id}: {e}"
        )


def calculate_loan_approved_volume_score(customer_id):
    try:
        approved_limit = Customer.objects.get(pk=customer_id).approved_limit
        max_loan_amount = Loan.objects.filter(customer_id=customer_id).aggregate(
            min_loan_amount=Min("loan_amount")
        )["min_loan_amount"]

        if max_loan_amount is not None:
            return round(
                (min(max_loan_amount, approved_limit) / approved_limit) * 100, 2
            )
        else:
            return 0.0
    except ObjectDoesNotExist:
        logger.error(f"Customer or loan not found for customer {customer_id}")

    except Exception as e:
        logger.error(
            f"Error calculating loan approved volume score for customer {customer_id}: {e}"
        )


def calculate_interest_rate(id, credit_score):
    try:
        if credit_score > 50:
            return 0.0
        elif 50 > credit_score > 30:
            return 12.0
        elif 30 > credit_score > 10:
            return 16.0
        else:
            return None

    except Exception as e:
        logger.error(
            f"Error calculating interest rates for customer {id}: {e}")


def loan_approval_status(id, credit_score):
    if credit_score < 10 or check_loan_limit_exceeded(id) or check_emi_limit_exceeded(id):
        return False
    else:
        return True


def get_count_of_loans(id):
    try:
        return Loan.objects.filter(customer_id=id).count()
    except Exception as e:
        logger.error(
            f"Error getting count of loans for customer {id}: {e}")


def check_loan_limit_exceeded(id):
    try:
        customer = Customer.objects.get(pk=id)
        approved_limit = customer.approved_limit

        current_loans_sum = Loan.objects.filter(customer_id=id).aggregate(
            sum_loan_amount=Sum('loan_amount'))['sum_loan_amount']

        return current_loans_sum > approved_limit

    except ObjectDoesNotExist:
        logger.error(f"Customer or loan not found for customer {id}")


def check_emi_limit_exceeded(id):
    try:
        customer = Customer.objects.get(pk=id)
        monthly_salary = customer.monthly_income

        current_emis_sum = Loan.objects.filter(id=id, is_approved=True).aggregate(
            sum_emis=Sum('monthly_installment'))['sum_emis']

        return current_emis_sum > 0.5 * monthly_salary

    except ObjectDoesNotExist:
        logger.error(f"Customer or loan not found for customer {id}")
