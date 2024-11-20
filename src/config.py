from pydantic_settings import BaseSettings


class Config(BaseSettings):
    # Define a `SECRET_KEY` environment variable and it will be used instead of the default here.
    secret_key: str = "my_top_secret_key"

    # API
    base_url: str = "http://localhost:8000"

    # Authentication
    access_token_expiration_hours: int = 24
    refresh_token_expiration_hours: int = 24

    # Passwords
    minimum_password_length: int = 10
    maximum_password_length: int = 128
    minimum_password_strength: float = 0.6

    # Usernames
    minimum_username_length: int = 3
    maximum_username_length: int = 24


config = Config()
