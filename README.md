# Fast API Users

Simple example of doing user registration, authentication, and login using FastAPI.

## Endpoints

`/register`: Creates a new user and sends an email verification.
`/verify_email`: Validates the token sent in the email verification and sets the user as verified.
`/resend_email_verification`: Create and resend email verification token.
`/login`: Login a given user and return access token + refresh token.
`/refresh_token`: Return a new access token given a refresh token.
`/change_password`: Change a user's password.