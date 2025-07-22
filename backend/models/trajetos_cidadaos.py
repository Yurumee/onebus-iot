from config import db
from typing import TYPE_CHECKING
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import ForeignKey, Integer

# if TYPE_CHECKING:
#     from models.trajeto import Trajeto
#     from models.cidadao import Cidadao

class TrajetosCidadaos(db.Model):
    __tablename__ = 'trajetos_cidadaos'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    cidadao_cpf: Mapped[str] = mapped_column(ForeignKey('cidadao.CPF'))
    trajeto_id: Mapped[int] = mapped_column(ForeignKey('trajeto.idTrajeto'))