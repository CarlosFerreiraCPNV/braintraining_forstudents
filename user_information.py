import bcrypt

def hash_password(password):
   password_bytes = password.encode('utf-8')
   hashed_bytes = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
   return hashed_bytes.decode('utf-8')

# Usage example
hashed_password = '$2b$12$RG6awkFm/nw2MfROMIanYeAXRheeBD0sJl6j0C1y2l7rCCsfUbJwO'
hashed_password_b = bytes(hashed_password, 'utf-8')

hashed = bcrypt.hashpw(hashed_password_b, bcrypt.gensalt())
print(hashed)
print(bcrypt.checkpw(hashed_password_b, hashed))
if bcrypt.checkpw(hashed_password_b, hashed):
    print("It Matches!")
else:
    print("It Does not Match :(")
