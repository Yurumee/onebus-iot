from config import db
from models.Usuario import Usuario
from models.Carro import Carro
# from models.Trajeto import Trajeto
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import Integer, String, ForeignKey
class Motorista(db.Model, Usuario):
    __tablename__ = 'motorista'

    CNH: Mapped[int] = mapped_column(Integer, primary_key=True)

    veiculoUsado: Mapped[str] = mapped_column(ForeignKey('carro.placa'))
    veiculoFK: Mapped['Carro'] = relationship('Carro', back_populates='motoristasFK')

    # trajetos: Mapped[List['Trajeto']] = relationship('Trajeto', back_populates='motorista')