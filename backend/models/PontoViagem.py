from config import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, Integer
import datetime

class PontoViagem(db.Model):
    __tablename__ = 'ponto_viagem'

    idPontoViagem: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    latitudePonto: Mapped[str] = mapped_column(String, nullable=False)
    longitutdePonto: Mapped[str] = mapped_column(String, nullable=False)
    data: Mapped[datetime.date] = mapped_column(nullable=False)
    hora: Mapped[datetime.time] = mapped_column(nullable=False)