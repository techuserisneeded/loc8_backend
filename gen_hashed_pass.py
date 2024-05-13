from bcrypt import hashpw, gensalt

password = '123456'
hashed_password = hashpw(password.encode('utf-8'), gensalt()).decode('utf-8')

print(hashed_password)
