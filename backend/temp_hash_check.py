from app.utils.security import hash_password

password_to_check = "password"
hashed_password = hash_password(password_to_check)
print(hashed_password) 