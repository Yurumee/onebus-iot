from config import db
from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, Integer

if TYPE_CHECKING:
    from models.trajeto import Trajeto

class PontoTrajeto(db.Model):
    __tablename__ = 'ponto_trajeto'

    idPontoTraj: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    latitude: Mapped[str] = mapped_column(String)
    longitude: Mapped[str] = mapped_column(String)

    # coluna de chave estrangeira
    trajeto_id: Mapped[int] = mapped_column(ForeignKey('trajeto.idTrajeto'))

    # relacionamento para acesso na via contrária
    # se comunica com o relacionamento com Trajeto trajeto_ponto
    # relacionamento 1 trajeto para N pontos
    # cada ponto tem apenas 1 trajeto
    trajeto: Mapped['Trajeto'] = relationship(back_populates='trajeto_ponto')