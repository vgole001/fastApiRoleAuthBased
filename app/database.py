from sqlmodel import Session, SQLModel, create_engine
from dotenv import load_dotenv
import os

# Use load_env to trace the path of .env file:
load_dotenv() 

POSTGRES_PORT       = os.environ["POSTGRES_PORT"]
POSTGRES_PASSWORD   = os.environ["POSTGRES_PASSWORD"]
POSTGRES_USER       = os.environ["POSTGRES_USER"]
POSTGRES_NAME       = os.environ["POSTGRES_NAME"]
POSTGRES_HOST       = os.environ["POSTGRES_HOST"]

# DATABASE_SCHEMA=carbon_footprint 
# DATABASE_TABLE=carbon_footprint

# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

SQLALCHEMY_DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_NAME}"
engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_size=50, echo = False )

# Dependency
def get_db():
    with Session(engine) as session:
        yield session
        
# Takes all classes that extend from Base Class and create them to database 
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
   
# Remove database file since sqlite gets created locally 
def shutdown():
    cwd = Path.cwd().resolve()
    db_file = [file for file in os.listdir() if file.endswith(".db")][0]
    os.remove(os.path.join(cwd, db_file))