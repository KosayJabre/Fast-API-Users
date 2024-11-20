# Fast API Users
A simple educational example for doing user registration, authentication, and login using FastAPI + SQLModel. 

Handles basic things like enforcing password strength, username profanity, and email address validation.

## Setup

To run the tests:
```
pytest .
```

To run the API locally:
```
uvicorn src.main:app --host 0.0.0.0 --port 8000
```

To run the API with Docker:
```
docker build . -t fast-api-users
docker run -p 8000:8000 fast-api-users
```

View the API spec and play around with it at: 
```
http://localhost:8000/docs
```


## Endpoints

- `/register`: Takes an email address, username, and password and creates user.
- `/login`: Takes a username/email + password, and returns an access token + refresh token.
- `/refresh_token`: Takes a refresh token and return a new access token + refresh token.
- `/change_password`: Change a user's password. Invalidates all previous tokens. 


