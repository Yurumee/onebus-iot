from config import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, Integer

class PontoTrajeto(db.Model):
    __tablename__ = 'ponto_trajeto'

    idPontoTraj: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    latitude: Mapped[str] = mapped_column(String, nullable=False)
    longitude: Mapped[str] = mapped_column(String, nullable=False)