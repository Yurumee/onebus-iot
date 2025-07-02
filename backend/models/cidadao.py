from config import db
from models.Usuario import Usuario
# from sqlalchemy.orm import mapped_column, Mapped

class Cidadao(db.Model, Usuario):
    __tablename__ = 'cidadao'