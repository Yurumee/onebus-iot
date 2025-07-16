from config import db
from typing import TYPE_CHECKING
# from datetime import datetime
import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, Integer

if TYPE_CHECKING:
    from models.motorista import Motorista
    from models.carro import Carro

class Trajeto(db.Model):
    __tablename__ = 'trajeto'

    idTrajeto: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    servicoPrestado: Mapped[str] = mapped_column(String(50), nullable=False)
    pontoOrigem: Mapped[str] = mapped_column(String(50), nullable=False)
    pontoDestino: Mapped[str] = mapped_column(String(50), nullable=False)
    horarioEstimado: Mapped[datetime.time] = mapped_column(nullable=False)
    
    # trajeto com um motorista
    # um motorista pode ter varios trajetos
    # motoristaResp: Mapped[int] = mapped_column(Integer, ForeignKey('motorista.cnh'))

    # trajeto com apenas um embarcado
    # um embarcado pode ter varios trajetos 
    # idEmbarcado: Mapped[str] = mapped_column(String, ForeignKey('carro.idEmbarcado'))

    # motorista: Mapped['Motorista'] = relationship('Motorista', back_populates='trajetos')
    # embarcado: Mapped['Carro'] = relationship('Carro', back_populates='trajetos')


