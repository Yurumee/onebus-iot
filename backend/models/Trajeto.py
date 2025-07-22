from config import db
from typing import TYPE_CHECKING
# from datetime import datetime
import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, Integer

if TYPE_CHECKING:
    from models.carro import Carro
    from models.pontoTrajeto import PontoTrajeto
    from models.cidadao import Cidadao

class Trajeto(db.Model):
    __tablename__ = 'trajeto'

    idTrajeto: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    servicoPrestado: Mapped[str] = mapped_column(String(50))
    pontoOrigem: Mapped[str] = mapped_column(String(50))
    pontoDestino: Mapped[str] = mapped_column(String(50))
    horarioEstimado: Mapped[datetime.time] = mapped_column()
    
    # coluna de chave estrangeira
    carro_placa: Mapped[str] = mapped_column(ForeignKey('carro.placa'))

    # relacionamento para acesso na via contrária
    # se comunica com o relacionamento com Carro trajeto
    # relacionamento 1 carro para N trajetos
    # cada trajeto tem apenas 1 carro
    carro: Mapped['Carro'] = relationship(back_populates='trajeto')

    # relacionamento N pontos de trajeto para 1 trajeto
    # cada trajeto pode ter vários pontos associados
    # ao ser cadastrado um novo ponto de trajeto nesse campo, ele se comunica com a coluna estrangeira da tabela trajeto
    trajeto_ponto: Mapped[list['PontoTrajeto']] = relationship()

    cidadaos: Mapped['Cidadao'] = relationship(secondary='trajetos_cidadaos')


