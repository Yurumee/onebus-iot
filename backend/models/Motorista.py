from config import db
from models.Usuario import Usuario
from models.Trajeto import Trajeto
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import Integer

class Motorista(db.Model, Usuario):
    __tablename__ = 'motorista'

    CNH: Mapped[int] = mapped_column(Integer, primary_key=True)

    motoristaPK: Mapped[Trajeto] = relationship(back_populates='motoristaFK')

