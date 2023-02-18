from dotenv import load_dotenv
import os
import jwt

load_dotenv()

JWT_SECRET = os.getenv("JWT_SECRET")
print(JWT_SECRET)
email = 'test@gmail.com'
username = 'test_user'

token = jwt.encode({"email": email, "username": username},
                   JWT_SECRET, algorithm="HS256")

print(token)
