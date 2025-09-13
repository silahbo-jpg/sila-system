"""
Email module for the SILA application.

This module provides email sending functionality with a mock implementation
for development and testing purposes.
"""
import logging
from typing import List, Optional, Dict, Any
from pydantic import EmailStr, BaseModel

# Get logger
logger = logging.getLogger(__name__)

class EmailMessage(BaseModel):
    """Email message model."""
    to: EmailStr | List[EmailStr]
    subject: str
    body: str
    html: Optional[str] = None
    cc: Optional[List[EmailStr]] = None
    bcc: Optional[List[EmailStr]] = None
    reply_to: Optional[EmailStr] = None
    attachments: Optional[List[Dict[str, Any]]] = None

def send_email(
    to: EmailStr | List[EmailStr],
    subject: str,
    body: str,
    html: Optional[str] = None,
    cc: Optional[List[EmailStr]] = None,
    bcc: Optional[List[EmailStr]] = None,
    reply_to: Optional[EmailStr] = None,
    attachments: Optional[List[Dict[str, Any]]] = None
) -> bool:
    """
    Send an email (mock implementation).
    
    In development and test environments, this logs the email instead of sending it.
    In production, this would connect to an actual email service.
    
    Args:
        to: Email recipient(s)
        subject: Email subject
        body: Plain text email body
        html: Optional HTML email body
        cc: Optional CC recipients
        bcc: Optional BCC recipients
        reply_to: Optional reply-to address
        attachments: Optional list of attachment dictionaries with 'filename' and 'content' keys
        
    Returns:
        bool: Always returns True in mock implementation
    """
    # Create email message
    email = EmailMessage(
        to=to,
        subject=subject,
        body=body,
        html=html,
        cc=cc,
        bcc=bcc,
        reply_to=reply_to,
        attachments=attachments or []
    )
    
    # Log the email instead of sending it
    logger.info(
        "[MOCK EMAIL] Email would be sent:\n"
        f"To: {email.to}\n"
        f"Subject: {email.subject}\n"
        f"Body: {email.body}\n"
        f"CC: {email.cc or 'None'}\n"
        f"BCC: {email.bcc or 'None'}\n"
        f"Reply-To: {email.reply_to or 'None'}\n"
        f"Attachments: {len(email.attachments or [])} files"
    )
    
    # Log each attachment (without content)
    for i, attachment in enumerate(email.attachments or [], 1):
        logger.info(
            f"  Attachment {i}: {attachment.get('filename', 'unnamed')} "
            f"({len(attachment.get('content', ''))} bytes)"
        )
    
    # In a real implementation, we would connect to an email service here
    # and return True/False based on success/failure
    return True

# For backward compatibility with existing code
send_mail = send_email

# Example usage:
if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    
    # Send a test email
    send_email(
        to="test@example.com",
        subject="Test Email",
        body="This is a test email from the mock email service.",
        html="<p>This is a <strong>test email</strong> from the mock email service.</p>"
    )
