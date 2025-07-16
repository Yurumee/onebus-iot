from config import db
from typing import TYPE_CHECKING, Optional
from models.usuario import Usuario
# from models.carro import Carro
# from models.Trajeto import Trajeto
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import Integer, String, ForeignKey

if TYPE_CHECKING:
    from models.carro import Carro
class Motorista(db.Model, Usuario):
    __tablename__ = 'motorista'

    cnh: Mapped[int] = mapped_column(Integer, primary_key=True)

    veiculoUsado: Mapped['Carro'] = relationship()

    # veiculoUsado: Mapped[Optional[str]] = mapped_column(ForeignKey('carro.placa'))