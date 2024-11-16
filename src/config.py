from pydantic_settings import BaseSettings


class Config(BaseSettings):
    # Do not rely on default value. 
    # Define a `SECRET_KEY` environment variable instead, and it will be used instead.
    secret_key: str = "my_top_secret_key"  
    
    # Authentication
    access_token_expiration_hours: int = 24
    refresh_token_expiration_hours: int = 24
    email_verification_token_expiration_hours: int = 24
    password_reset_token_expiration_hours: int = 24
    
    # Passwords
    minimum_password_length: int = 10
    maximum_password_length = 128
    minimum_password_strength: float = 0.6
    
    # Usernames
    minimum_username_length: int = 3
    maximum_username_length: int = 24


config = Config()