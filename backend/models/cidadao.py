from config import db
from typing import TYPE_CHECKING
from models.usuario import Usuario
from sqlalchemy.orm import mapped_column, Mapped, relationship

if TYPE_CHECKING:
    from models.trajeto import Trajeto
class Cidadao(db.Model, Usuario):
    __tablename__ = 'cidadao'

    trajetos: Mapped['Trajeto'] = relationship(secondary='trajetos_cidadaos')