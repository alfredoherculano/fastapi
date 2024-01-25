'''
Defines the schemas with the specific 
data the client has to provide.
'''

from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, Literal

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True # If the user doesn't provide a value it's going to defaut to true


class PostCreate(PostBase):
    pass


class UserResponse(BaseModel):
    id: int
    created_at: datetime
    email: EmailStr
    class Config:
        orm_mode = True


 # It is also interesintg to define a model for a response to be sent back to the client,
 # so that we only show the user what we want them to see

class PostResponse(PostBase):
    id: int
    created_at: datetime
    owner_id: int       # We don't add this field in the parent class because we don't want the user to have to 
                        # provide the owner_id everytime he wants to access a post.
    owner: UserResponse

    class Config:       # Explanation: https://fastapi.tiangolo.com/tutorial/sql-databases/#create-pydantic-models-schemas-for-reading-returning
                        # https://youtu.be/0sOvCWFmrtA?t=20417
        orm_mode = True


class PostOut(BaseModel):
    Post: PostResponse
    votes: int
    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    email: EmailStr         # Pydantic lib that checks if the user provided a valid email
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None


class Vote(BaseModel):
    post_id: int
    dir: Literal[0, 1]      # Validates that the only allowed integers are 0 or 1