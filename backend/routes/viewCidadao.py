from config import app, db
from flask import Blueprint, request
from models.Cidadao import Cidadao

view_cidadao = Blueprint('view_cidadao', __name__)

@app.route('/cidadao')
def home_cidadao():
    # cnh = 1234567890
    cpf = '789.456.123-00'
    nome = 'Alice Mock'
    senhaTop = 'senhaforte123'

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

    return "Página principal do cidadão"

@app.route('/signin', methods=['GET', 'POST'])
def singin():
    # if request.method == 'POST':
        # cpf = request.form.get('cpf')
        # password = request.form.get('senha')
    cpf = '789.456.123-00'
    password = 'senhaforte123'

    user = Cidadao.query.filter_by(CPF=cpf).first()

    if user:
        if user.senha == password:
            return 'SENHA OK'
        else:
            return 'ALGO DEU ERRADO'

    return 'USUARIO NON ECZISTEH'