# CreditApprovalSystem 🤑
Introducing our Credit Approval System, a financial tool that assesses a customer's creditworthiness by analyzing historical data. The system calculates an individual credit score and evaluates eligibility for processing specific loan amounts.

## Installation 💻

Provide step-by-step instructions on how to install the project.
1. Clone git repository
2. Install docker
3. Run the command to build a docker image of the project
   ```
   $ docker build .
5. Create and run container using following command
   ```
   $ docker-compose up -d
6. Now ready to hit end points at `localhost:8000`

## Endpoints ⚡
### 1. Create Customer

- **Endpoint:** http://127.0.0.1:8000/api/register/
- **Request Format:**
  ```json
  {
    "first_name": "",
    "last_name": "",
    "age": "",
    "phone_number": "",
    "monthly_income": ""
  }
- **Response Format:**
  ```json
  {
    "customer_id": ,
    "name": "",
    "age": ,
    "monthly_income": ,
    "approved_limit": ,
    "phone_number": 
  }
### 2. Check Eligibility

- **Endpoint:** http://127.0.0.1:8000/api/check-eligibility/
- **Request Format:**
  ```json
  {
    "customer_id":"",
    "loan_amount":,
    "interest_rate":,
    "tenure":
  }
- **Response Format:**
  ```json
  {
    "customer_id": "",
    "approval": ,
    "interest_rate": ,
    "corrected_interest_rate": ,
    "tenure": ,
    "monthly_installment": 
  }
### 3. Create Loan

- **Endpoint:** http://127.0.0.1:8000/api/create-loan/
- **Request Format:**
  ```json
  {
    "customer_id":"",
    "loan_amount":,
    "interest_rate":,
    "tenure":
  }
- **Response Format:**
  ```json
  {
    "loan_id": ,
    "customer_id": ,
    "loan_approved": ,
    "message": ,
    "monthly_installment": 
  }
### 4. View Loan by loan ID

- **Endpoint:** http://127.0.0.1:8000/api/view-loan/?loan_id=
- **Response Format:**
  ```json
  {
    "id": ,
    "loan_amount": ,
    "interest_rate": ,
    "monthly_installment": ,
    "tenure": ,
    "customer": {
        "id": ,
        "first_name": "",
        "last_name": "",
        "phone_number": ,
        "age": 
    }
  }
### 5. View Loan by customer ID

- **Endpoint:** http://127.0.0.1:8000/api/view-loan/?customer_id=
- **Response Format:**
  ```json
  [
    {
        "id": ,
        "loan_amount": ,
        "interest_rate": ,
        "monthly_installment": ,
        "repayments_left": 
    },
  ]

  




