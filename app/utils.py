'''
Holds a bunch of utility functions
'''

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") # Telling passlib which encryption algorithm to use (bcrypt)

def hash(password: str):
    return pwd_context.hash(password)


# Function to get the raw password, hash it, and then compare to the hash in the database

def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)