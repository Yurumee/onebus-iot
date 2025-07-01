from config import app, db
from flask import Blueprint
from models.Motorista import Motorista
from sqlalchemy import or_

view_motorista = Blueprint('view_motorista', __name__)

@app.route('/')
def home():
    cnh = 1234567890
    cpf = '123.456.789-00'
    nome = 'Alice Mock'
    senhaTop = 'senhamuitoforte123'

    if Motorista.query.filter(or_(Motorista.CNH==cnh, Motorista.CPF==cpf)).first():
        return 'MOTORISTA JÁ CADASTRADO'

    MOCKtorista = Motorista(
        CNH=cnh,
        CPF=cpf,
        nomeCompleto=nome,
        senha=senhaTop
    )

    db.session.add(MOCKtorista)
    db.session.commit()

    return "AEEEEE"

