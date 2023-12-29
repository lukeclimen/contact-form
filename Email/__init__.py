import os
import datetime
from typing import Any

from azure.communication.email import EmailClient
from azure.core.credentials import AzureKeyCredential

internal_email_address = os.getenv('INTERNAL_EMAIL_ADDRESS')
system_email_address = os.getenv('SYSTEM_EMAIL_ADDRESS')
email_communication_endpoint = os.getenv('AZURE_COMMUNICATIONS_ENDPOINT')
email_communication_key = os.getenv('AZURE_COMMUNICATIONS_KEY')


def _send_email(email: dict[str, Any]) -> None:
    """Sends an email using Azure Communication Services"""
    try:
        client = EmailClient(email_communication_endpoint, AzureKeyCredential(email_communication_key))
        poller = client.begin_send(email)
        result = poller.result()
    except Exception as ex:
        raise Exception(ex)


def _create_internal_email(name: str, email: str, message: str) -> dict[str, any]:
    """Crafts the email copy for the internally-sent email"""
    
    timestamp = datetime.datetime.now()
    html_email_content = f"""<p>Hello,</p>
    
    <p>The contact form has been filled out by {name} ({email}) at {timestamp} UTC.</p>

    <p>The message that {name} submitted was:</p>

    <p>{message}</p>
    """
    plain_text_email_content = f"""Hello,
    
    The contact form has been filled out by {name} ({email}) at {timestamp} UTC.

    The message that {name} submitted was:

    {message}
    """

    return {
        "content": {
            "subject": "New Contact Form Submission",  # Subject of the email message. Required.
            "html": html_email_content,  # Optional. Html version of the email message.
            "plainText": plain_text_email_content  # Optional. Plain text version of the email message.
        },
        "recipients": {
            "to": [
                {
                    "address": internal_email_address,  # Email address. Required.
                    "displayName": "Internal Email Address"  # Optional. Email display name.
                }
            ]
        },
        "senderAddress": system_email_address,  # Sender email address from a verified domain. Required.
    }


def _create_acknowledgement_email(name: str, email: str, message: str) -> dict[str, Any]:
    """Crafts the acknowledgement email sent to the person who submitted the form"""

    html_email_content = f"""<p>Hello {name},</p>
    
    <p>You are receiving this email to confirm that the contact form you filled out at
    lukeclimenhage.com has been received! If any follow-up is required, an email will
    be sent to you directly.</p>

    <p>Please don't respond to this email, as this email's inbox is not monitored.</p>

    <p>Have a great day!</p>

    <p>Luke Climenhage</p>
    """
    plain_text_email_content = f"""Hello {name},
    
    You are receiving this email to confirm that the contact form you filled out at
    lukeclimenhage.com has been received! If any follow-up is required, an email will
    be sent to you directly.

    Please don't respond to this email, as this email's inbox is not monitored.

    Have a great day!

    Luke Climenhage
    """

    return {
        "content": {
            "subject": "Contact form submission received",  # Subject of the email message. Required.
            "html": html_email_content,  # Optional. Html version of the email message.
            "plainText": plain_text_email_content  # Optional. Plain text version of the email message.
        },
        "recipients": {
            "to": [
                {
                    "address": email,  # Email address. Required.
                    "displayName": name  # Optional. Email display name.
                }
            ]
        },
        "senderAddress": system_email_address,  # Sender email address from a verified domain. Required.
    }