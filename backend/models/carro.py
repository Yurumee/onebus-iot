from config import db
from models.Trajeto import Trajeto
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import String
from typing import List

class Carro(db.Model):
    __tablename__ = 'carro'

    idEmbarcado: Mapped[str] = mapped_column(String, primary_key=True)
    placa: Mapped[str] = mapped_column(String(7), nullable=False)
    tipoVeiculo: Mapped[str] = mapped_column(String(20), nullable=False)
    
    trajetos: Mapped[List[Trajeto]] = relationship(Trajeto, back_populates='embarcado')
