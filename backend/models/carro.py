from config import db
from models.Trajeto import Trajeto
from models.Motorista import Motorista
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import String, Integer, ForeignKey
from typing import List

class Carro(db.Model):
    __tablename__ = 'carro'

    # idEmbarcado: Mapped[str] = mapped_column(String, primary_key=True)
    placa: Mapped[str] = mapped_column(String(7), primary_key=True)
    latitudeAtual: Mapped[str] = mapped_column(String, nullable=False)
    longitudeAtual: Mapped[str] = mapped_column(String, nullable=False)
    tipoVeiculo: Mapped[str] = mapped_column(String(20), nullable=False)

    motoristas: Mapped[int] = mapped_column(ForeignKey('motorista.CNH'))
    motoristasFK: Mapped[List['Motorista']] = relationship('Motorista', back_populates='veiculoFK')
    
    # trajetos: Mapped[List['Trajeto']] = relationship('Trajeto', back_populates='embarcado')
