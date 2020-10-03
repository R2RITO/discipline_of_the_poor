"""
Module used to provide functions that notify when the budget is low
on money
"""
from budget.utils.email_utils import send_email


def notify_low_available_amount(budget):
    """
    Notifies when the budget's amount is low through an email
    :param Budget budget: The budget whose amount is low
    :return:
    """
    format_params = {
        'budget_name': budget.description,
        'budget_available_amount': budget.available_amount
    }
    recipient = budget.owner.email

    subject = 'Budget with low available amount'

    text_body = """\
        Hello, your budget {budget_name} has an available 
        amount of {budget_available_amount}.
    """.format(**format_params)

    html_body = """\
    <html>
        <body>
            <p>
                Hello<br>
                Your budget {budget_name} has an available 
                amount of {budget_available_amount}.
            </p>
        </body>
    </html>
    """.format(**format_params)

    send_email(
        recipient=recipient,
        subject=subject,
        text_body=text_body,
        html_body=html_body
    )
