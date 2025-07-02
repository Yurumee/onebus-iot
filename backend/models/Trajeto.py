from config import db
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

    motoristaResp: Mapped[str] = mapped_column(ForeignKey('motorista.CPF'))
    placaCarro: Mapped[str] = mapped_column(ForeignKey('carro.placa'))

    motoristaFK: Mapped[Motorista] = relationship(back_populates='motoristaPK')
    placaCarroFK: Mapped[Carro] = relationship(back_populates='placaCarroPK')


