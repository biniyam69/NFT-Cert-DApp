from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()




def get_db():
    engine = create_engine("postgresql://POSTGRES_USER:POSTGRES_PASSWORD@db:5432/POSTGRES_DB")
