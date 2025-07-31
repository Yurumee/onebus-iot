from config import db, app
from flask import Blueprint, jsonify
from models.carro import Carro

view_carro = Blueprint('view_carro', __name__)

@view_carro.route('/', methods=['GET', 'POST'])
def post_new_car():
    """
    Rota para cadastrar carros de exemplo no banco de dados.

    Método:
        GET, POST

    Retorno:
        Uma mensagem indicando que os carros foram cadastrados ou já existem.
    
    Observação:
        Esta rota insere dois carros mockados no banco de dados para fins de teste.
    """
    carros_mock = [
        {"placa": "4N4L1C3", "tipo": "Carro"},
        {"placa": "S54NT05", "tipo": "Van"}
    ]
    cadastrados = []
    ja_existentes = []

    for carro in carros_mock:
        placa = carro["placa"]
        tipo = carro["tipo"]
        existe = Carro.query.filter_by(placa=placa).first()
        if existe:
            ja_existentes.append(placa)
        else:
            novo_carro = Carro(placa=placa, tipoVeiculo=tipo)
            db.session.add(novo_carro)
            cadastrados.append(placa)

    db.session.commit()

    mensagem = ""
    if cadastrados:
        mensagem += f"Carros cadastrados: {', '.join(cadastrados)}.\n"
    if ja_existentes:
        mensagem += f"Carros já existentes: {', '.join(ja_existentes)}."

    return mensagem.strip()

