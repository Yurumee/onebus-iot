from config import app, db
from flask import Blueprint
from models.Cidadao import Cidadao

view_cidadao = Blueprint('view_cidadao', __name__)

@app.route('/cidadao')
def home_cidadao():
    # cnh = 1234567890
    cpf = '123.456.789-00'
    nome = 'Alice Mock'
    senhaTop = 'senhamuitoforte123'

    if Cidadao.query.filter_by(CPF=cpf).first():
        return 'CIDADAO JÁ CADASTRADO'

    MOCKCidadao = Cidadao(
        # CNH=cnh,
        CPF=cpf,
        nomeCompleto=nome,
        senha=senhaTop
    )

    db.session.add(MOCKCidadao)
    db.session.commit()

    return "AEEEEE"

