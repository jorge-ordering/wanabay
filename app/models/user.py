
from distutils.command.config import config
from sqlalchemy import Boolean, Column, Integer, String,DateTime
from sqlalchemy_utils import EmailType
import datetime

from configs.base_class import Base


class User(Base):
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime,default=datetime.datetime.utcnow)
    email = Column(EmailType)
    username = Column(String, unique=True)
    hashed_password = Column(String)
    enabled = Column(Boolean,default=True)
