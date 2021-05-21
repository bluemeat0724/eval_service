from app.models import db,Base
from sqlalchemy import Column,String,Integer,Float,TEXT,JSON

class Answers(Base):
    __tablename__ = 'answers'
    answer = Column(JSON)
    code = Column(String(64))


