from config import db
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import String

class Carro(db.Model):
    __tablename__ = 'Carro'

    idEmbarcado: Mapped[str] = mapped_column(String(30), primary_key=True)
    placa: Mapped[str] = mapped_column(String(7), nullable=False)
    tipoVeiculo: Mapped[str] = mapped_column(String(20), nullable=False)
    
