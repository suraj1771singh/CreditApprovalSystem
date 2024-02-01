from celery import shared_task
import pandas as pd
from .models import Customer, Loan

FILE_PATH_1 = 'customer_data.xlsx'
FILE_PATH_2 = 'loan_data.xlsx'


@shared_task
def import_excel_data():
    try:
        df = pd.read_excel(FILE_PATH_1)

        # Loop through each row and create Customer instances
        for _, row in df.iterrows():
            customer = Customer(
                first_name=row['First Name'],
                last_name=row['Last Name'],
                age=row['Age'],
                phone_number=row['Phone Number'],
                monthly_income=row['Monthly Salary'],
                approved_limit=row['Approved Limit'],
            )

            customer.save()

        df = pd.read_excel(FILE_PATH_2)
        # Loop through each row and create loan instances
        for _, row in df.iterrows():
            loan = Loan(
                customer_id=row['Customer ID'],
                loan_amount=row['Loan Amount'],
                tenure=row['Tenure'],
                interest_rate=row['Interest Rate'],
                monthly_installment=row['Monthly payment'],
                emis_paid_on_time=row['EMIs paid on Time'],
                approval_date=row['Date of Approval'],
                end_date=row['End Date'],
            )

            loan.save()

    except Exception as e:
        print(f"Error importing data: {e}")
