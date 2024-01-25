'''
Handles user credentials verification
'''

from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import database, oauth2, schemas, models, utils

router = APIRouter(tags=["Authentication"])

@router.post('/login', response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):

    # OAuth2PasswordRequestForm required fiels are "username" and "password",
    # that's why, in the code below, we compare the "email" field from our models with "username".
    
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")
    
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    
    # create token
    # return token

    access_token = oauth2.create_access_token(data = {"user_id": user.id}) # The content of the dictionary is the information we want
                                                                          # to provide about the user, it can also have a "role"
                                                                          # or other fields.

    return {"access_token": access_token, "token_type": "bearer"}