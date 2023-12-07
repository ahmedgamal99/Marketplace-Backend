from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import os
from dotenv import load_dotenv

load_dotenv()

if os.environ['ENVIRON'] == 'PROD':
    DATABASE_URL = os.environ['PROD_URL']
else:
    DATABASE_URL = os.environ['DATABASE_URL']

# DATABASE_URL = os.environ['DATABASE_URL']
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    except:
        db.close()
