from config import db
# from models import Motorista, Carro
from models.Motorista import Motorista
from models.Carro import Carro
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey

class Trajeto(db.Model):
    __tablename__ = 'trajeto'

    servicoPrestado: Mapped[str] = mapped_column(String(50), nullable=False)
    origem: Mapped[str] = mapped_column(String(50), nullable=False)
    destino: Mapped[str] = mapped_column(String(50), nullable=False)
    kmEstimado: Mapped[str] = mapped_column(String(50), nullable=False)

    # trajeto com um motorista
    # um motorista pode ter varios trajetos
    motoristaResp: Mapped[str] = mapped_column(ForeignKey('motorista.CNH'))

    # trajeto com apenas um embarcado
    # um embarcado pode ter varios trajetos 
    idCarro: Mapped[str] = mapped_column(ForeignKey('carro.idEmbarcado'))

    motoristaFK: Mapped[Motorista] = relationship(back_populates='motoristaPK')
    idEmbarcadoFK: Mapped[Carro] = relationship(back_populates='idEmbarcadoPK')


