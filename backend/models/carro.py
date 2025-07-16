from config import db
from typing import TYPE_CHECKING, Optional
# from models.trajeto import Trajeto
# from models.motorista import Motorista
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import String, Integer, ForeignKey

if TYPE_CHECKING:
    from models.motorista import Motorista

class Carro(db.Model):
    __tablename__ = 'carro'

    # idEmbarcado: Mapped[str] = mapped_column(String, primary_key=True)
    placa: Mapped[str] = mapped_column(String(7), primary_key=True)
    latitudeAtual: Mapped[Optional[str]] = mapped_column(String)
    longitudeAtual: Mapped[Optional[str]] = mapped_column(String)
    tipoVeiculo: Mapped[str] = mapped_column(String(20), nullable=False)

    motorista_cnh: Mapped[Optional[str]] = mapped_column(ForeignKey('motorista.cnh'))
    motorista: Mapped[list['Motorista']] = relationship(back_populates='veiculoUsado', uselist=True)
