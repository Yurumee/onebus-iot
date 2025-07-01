from config import db
from models.Usuario import Usuario
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import Integer

class Motorista(db.Model, Usuario):
    __tablename__ = 'Motorista'

    CNH: Mapped[int] = mapped_column(Integer, primary_key=True)
    # CPF: Mapped[str] = mapped_column(String(14), unique=True, nullable=False)
    # nomeCompleto: Mapped[str] = mapped_column(String(80), nullable=False)
    # senha: Mapped[str] = mapped_column(String(20), nullable=False)

