'''
Defines the models with which the
ORM (in this case SQLAlchemy) will use to
communicate with the datebase.
'''

from sqlalchemy import TIMESTAMP, Boolean, Column, ForeignKey, Integer, String, text
from sqlalchemy.orm import relationship
from .database import Base

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='TRUE', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    owner = relationship("User") # This is an SQLAlchemy functionality to create a relationship between models,
                                 # and has nothing to do with table raltions in our database.

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    phone_number = Column(String, nullable=True)

class Vote(Base):
    __tablename__ = "votes"

    posts_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True, nullable=False)
    users_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True, nullable=False)
