from postmarker.core import PostmarkClient

from src.utils.auth import create_email_verification_token
from src.utils.email_addresses import is_valid_email_address


SERVER_TOKEN = "server-token-here"  
NO_REPLY_ADDRESS = "noreply@webvoter.io"


postmark = PostmarkClient(server_token=SERVER_TOKEN)


def send_registration_email(recipient_email: str):
    verification_token = create_email_verification_token(recipient_email)

    if is_valid_email_address(recipient_email):
        postmark.emails.send(
            From=NO_REPLY_ADDRESS,
            To=recipient_email,
            Subject="Welcome to WebVoter",
            HtmlBody=f"Foo bar. Verification token: {verification_token}",
        )


def send_password_reset_email(recipient_email: str, token: str):
    if is_valid_email_address(recipient_email):
        reset_link = f"http://webvoter.io/reset-password?token={token}"  # Adjust the URL as needed
        postmark.emails.send(
            From=NO_REPLY_ADDRESS,
            To=recipient_email,
            Subject="Password Reset Request",
            HtmlBody=f"Click on the link to reset your password: {reset_link}",
        )
