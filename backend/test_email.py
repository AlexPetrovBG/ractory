from pydantic import BaseModel, EmailStr

class User(BaseModel):
    email: EmailStr

# Test valid email
user = User(email='test@example.com')
print(f"Valid email: {user.email}")

# This would raise a validation error if email-validator is working
try:
    invalid_user = User(email='not-an-email')
    print("FAILURE: Invalid email was accepted")
except Exception as e:
    print(f"SUCCESS: Invalid email was rejected: {e}")
