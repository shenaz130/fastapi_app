from passlib.context import CryptContext


# Define the context to support bcrypt or other algorithms
pwd_context = CryptContext(schemes=["bcrypt", "argon2", "sha256_crypt"], deprecated="auto")

#hashing the password
def hash(password: str):
    return pwd_context.hash(password)

# Verify the password
def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
    




