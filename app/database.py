'''
Code SQLAlchemy uses to connect with
the specified database.
'''

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings
# import psycopg # This is the Postgres database driver, which allow us to communicate with the databse
# from psycopg.rows import dict_row # Used to display column names in the JSON
# import time

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


'''
The code below is not being used, it's left here as reference, 
in case we want to use raw SQL with Psycopg instead of an ORM like SQLAlchemy.
'''

# A connection to a database can potentially fail (either to a wrong password or something else)
# so we'll use try/except to try to connect to it.

# while True: # Putting it inside a loop so that the code after it isn't run unless the connection is estabilished
#     try:
#         conn = psycopg.connect(host='localhost', dbname='fastapi', user='postgres', password='alfre_postgres', row_factory=dict_row)
#         cursor = conn.cursor()
#         print("Database connection was successfull!")
#         break

#     except Exception as error:
#         print("Connecting to database failed.")
#         print("Error: ", error)
#         time.sleep(2) # Wait 2 seconds before trying to connect again