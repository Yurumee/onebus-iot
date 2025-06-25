from config import db
from sqlalchemy.orm import mapped_column
from sqlalchemy import String, Integer

class Motorista(db.Model):
    __tablename__ = 'Motorista'

    