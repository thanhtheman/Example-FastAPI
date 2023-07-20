from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()



#set up a connection to the database
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


#set up psycopg2 - that runs raw SQL command without SQLAlchemy
# try:
#     conn = psycopg2.connect(host="localhost", database="postgres", user="postgres", 
#                             password="OhYeah123", cursor_factory=RealDictCursor)
#     cursor = conn.cursor()
#     print("database connected!")
# except Exception as error:
#     print("failed to connect to database")
#     print(error)