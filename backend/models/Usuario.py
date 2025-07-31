from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import String

class Usuario():
    cpf: Mapped[str] = mapped_column(String(14), primary_key=True)
    nome_completo: Mapped[str] = mapped_column(String(80))
    senha: Mapped[str] = mapped_column(String(30))
    tipo_usuario: Mapped[str] = mapped_column(String(20))