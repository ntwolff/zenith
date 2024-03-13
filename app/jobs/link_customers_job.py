from app.services.customer_service import CustomerService

def run_link_customers_job():
    customer_service = CustomerService()

    # Fetch distinct PII values from the customer database
    pii_types = ['email', 'phone', 'ssn']
    for pii_type in pii_types:
        pii_values = customer_service.get_distinct_pii_values(pii_type)
        for pii_value in pii_values:
            customer_service.link_customers_by_pii(pii_type, pii_value)