from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from configs.settings import DATABASE_HOST, DATABASE_NAME, DATABASE_USERNAME, DATABASE_PASSWORD
# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
SQLALCHEMY_DATABASE_URL = f"postgresql://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_HOST}/{DATABASE_NAME}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
