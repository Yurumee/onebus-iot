from config import db
from typing import TYPE_CHECKING, Optional
from models.usuario import Usuario
# from models.carro import Carro
# from models.Trajeto import Trajeto
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import Integer, String, ForeignKey, Column

if TYPE_CHECKING:
    from models.carro import Carro
class Motorista(db.Model, Usuario):
    __tablename__ = 'motorista'

    cnh: Mapped[int] = mapped_column(Integer, primary_key=True)
    # coluna de chave estrangeira
    carro_placa: Mapped[Optional[str]] = mapped_column(ForeignKey('carro.placa'))

    # relacionamento para acesso na via contrária
    # se comunica com o relacionamento com Carro motorista_cnh
    # relacionamento 1 carro para N motoristas
    # cada motorista tem apenas 1 carro
    carro: Mapped['Carro'] = relationship(back_populates='motorista_cnh')