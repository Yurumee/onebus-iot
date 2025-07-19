from config import db
from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, Integer
import datetime

if TYPE_CHECKING:
    from models.carro import Carro

class PontoViagem(db.Model):
    __tablename__ = 'ponto_viagem'

    idPontoViagem: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    latitudePonto: Mapped[str] = mapped_column(String)
    longitutdePonto: Mapped[str] = mapped_column(String)
    data: Mapped[datetime.date] = mapped_column()
    hora: Mapped[datetime.time] = mapped_column()

    carro_placa: Mapped[str] = mapped_column(ForeignKey('carro.placa'))

    # relacionamento para acesso na via contrária
    # se comunica com o relacionamento com Carro viagem_pontos
    # relacionamento 1 carro para N pontos
    # cada ponto tem apenas 1 carro
    carro: Mapped['Carro'] = relationship(back_populates='viagem_pontos')