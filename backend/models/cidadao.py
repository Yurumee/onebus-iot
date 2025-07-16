from config import db
from models.usuario import Usuario
# from sqlalchemy.orm import mapped_column, Mapped

class Cidadao(db.Model, Usuario):
    __tablename__ = 'cidadao'