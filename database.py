from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# format: postgresql+psycopg://USER:PASSWORD@HOST:PORT/DATABASE
DATABASE_URL = "postgresql+psycopg://postgres:root@localhost:5432/fastapi_db"

engine = create_engine(DATABASE_URL)                     # the connection
SessionLocal = sessionmaker(bind=engine, autoflush=False) # makes sessions
Base = declarative_base()                                # parent class for tables