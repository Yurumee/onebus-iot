from config import db
from typing import TYPE_CHECKING
# from datetime import datetime
import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, Integer

if TYPE_CHECKING:
    from models.Motorista import Motorista
    from models.Carro import Carro

class Trajeto(db.Model):
    __tablename__ = 'trajeto'

    idTrajeto: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    servicoPrestado: Mapped[str] = mapped_column(String(50), nullable=False)
    origem: Mapped[str] = mapped_column(String(50), nullable=False)
    destino: Mapped[str] = mapped_column(String(50), nullable=False)
    kmEstimado: Mapped[str] = mapped_column(String(50), nullable=False)
    horarioInicio: Mapped[datetime.time] = mapped_column()
    horarioFim: Mapped[datetime.time] = mapped_column()


    # trajeto com um motorista
    # um motorista pode ter varios trajetos
    motoristaResp: Mapped[int] = mapped_column(Integer, ForeignKey('motorista.CNH'))

    # trajeto com apenas um embarcado
    # um embarcado pode ter varios trajetos 
    idEmbarcado: Mapped[str] = mapped_column(String, ForeignKey('carro.idEmbarcado'))

    motorista: Mapped['Motorista'] = relationship('Motorista', back_populates='trajetos')
    embarcado: Mapped['Carro'] = relationship('Carro', back_populates='trajetos')


