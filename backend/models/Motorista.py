from config import db
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import String, Integer

class Motorista(db.Model):
    __tablename__ = 'Motorista'

    CNH: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True)
    CPF: Mapped[str] = mapped_column(String(11), unique=True, nullable=False)
    nomeCompleto: Mapped[str] = mapped_column(String(80), nullable=False)
    senha: Mapped[str] = mapped_column(String(20), nullable=False)

