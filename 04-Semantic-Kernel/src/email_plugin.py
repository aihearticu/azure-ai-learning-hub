from typing import Annotated
from semantic_kernel.functions import kernel_function

class EmailPlugin:
    """
    Email plugin for sending expense claim emails.
    This is a mock implementation for the lab.
    """
    
    @kernel_function(
        name="send_email",
        description="Send an email with expense claim details"
    )
    def send_email(
        self,
        to: Annotated[str, "The recipient email address"],
        subject: Annotated[str, "The email subject"],
        body: Annotated[str, "The email body containing expense details"]
    ) -> str:
        """
        Simulates sending an email with expense claim details.
        
        Args:
            to: Recipient email address
            subject: Email subject
            body: Email body with expense details
            
        Returns:
            Confirmation message
        """
        print(f"\n{'='*50}")
        print(f"SENDING EMAIL (Simulated)")
        print(f"{'='*50}")
        print(f"To: {to}")
        print(f"Subject: {subject}")
        print(f"Body:\n{body}")
        print(f"{'='*50}\n")
        
        return f"Email successfully sent to {to} with subject: {subject}"
    
    @kernel_function(
        name="format_expense_summary",
        description="Format expense details into a professional email format"
    )
    def format_expense_summary(
        self,
        expenses: Annotated[str, "List of expenses with details"],
        total_amount: Annotated[float, "Total amount of all expenses"],
        employee_name: Annotated[str, "Name of the employee submitting expenses"]
    ) -> str:
        """
        Formats expense details into a professional email format.
        
        Args:
            expenses: String containing expense details
            total_amount: Total amount of expenses
            employee_name: Employee name
            
        Returns:
            Formatted email body
        """
        email_body = f"""Dear Finance Team,

I am submitting my expense claim for approval. Please find the details below:

Employee Name: {employee_name}

Expense Details:
{expenses}

Total Amount: ${total_amount:.2f}

All receipts are attached as per company policy.

Please process this expense claim at your earliest convenience.

Best regards,
{employee_name}
"""
        return email_body