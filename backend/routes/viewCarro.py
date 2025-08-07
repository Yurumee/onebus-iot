from config import db
from flask import Blueprint, jsonify, request, render_template
from models.carro import Carro
from models.motorista import Motorista
from models.trajeto import Trajeto

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
            novo_carro = Carro(placa=placa, tipo_veiculo=tipo)
            db.session.add(novo_carro)
            cadastrados.append(placa)

    db.session.commit()

    mensagem = ""
    if cadastrados:
        mensagem += f"Carros cadastrados: {', '.join(cadastrados)}.\n"
    if ja_existentes:
        mensagem += f"Carros já existentes: {', '.join(ja_existentes)}."

    return mensagem.strip()

@view_carro.route('/alterar-carro', methods=['GET', 'PATCH'])
def edit_carro():

    if request.method == 'PATCH':
        data = request.get_json()
        placa = data.get('placa-carro')

        try:
            carro_desejado = Carro.query.filter_by(placa=placa).first()
        except Exception as e:
            return  jsonify({
                "status":"error",
                "message":f"houve um erro {str(e)}"
            })
        
        if carro_desejado:
            new_placa = data.get('new-placa-carro')
            new_tipo_veiculo = data.get('tipo-veiculo')

            if new_placa != carro_desejado.placa and new_placa != None:
                trajetos = db.session.query(Trajeto).where(Trajeto.carro_placa == carro_desejado.placa)
                motoristas = db.session.query(Motorista).where(Motorista.carro_placa == carro_desejado.placa)
                carro_desejado.placa = new_placa

                for motorista in motoristas:
                    # motorista.carro_placa = new_placa
                    carro_desejado.motorista_cnh.append(motorista)
                
                for trajeto in trajetos:
                    carro_desejado.trajeto.append(trajeto)

                db.session.commit()

            if new_tipo_veiculo != carro_desejado.tipo_veiculo and new_tipo_veiculo != None:
                carro_desejado.tipo_veiculo = new_tipo_veiculo
                db.session.commit()

            return jsonify({
                "status":"success",
                "message":"updates realizados com sucesso"
            }), 200

        else:
            return jsonify({
                "status":"not found",
                "message":"carro nao encontrado"
            }), 404
    
    return render_template('pagina_editar_motorista.html'), 302