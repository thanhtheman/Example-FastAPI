from passlib.context import CryptContext #this is to hash the fucking password so we don't get hacked!

#this is to setup the hashing algorithm for our password
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(password: str):
    hashed_password = pwd_context.hash(password)
    return hashed_password

def user_verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)