from config import db, app
from flask import Blueprint, jsonify, render_template, request
# from sqlalchemy import select
from datetime import datetime
from models.trajeto import Trajeto
from models.pontoTrajeto import PontoTrajeto
from models.trajetos_cidadaos import TrajetosCidadaos
from models.motorista import Motorista

view_trajeto = Blueprint('view_trajeto', __name__)

@view_trajeto.route('/', methods=['GET', 'POST'])
def post_new_trajeto():
    """
    Rota para cadastrar um trajeto mockado no banco de dados.

    Métodos:
        GET, POST

    Retorno:
        - status, message e dados do trajeto.
        - status error se ocorrer exceção.
    """
    servico_prestado = request.form.get('servico-prestado')
    origem = request.form.get('origem')
    destino = request.form.get('destino')
    placa = request.form.get('placa')
    datahora_estimado = datetime.strptime(request.form.get('datahora-estimado'), "%Y-%m-%dT%H:%M:%S")
    # # print("datahora_estimado (datetime)=", datetime.strptime(datahora_estimado, "%Y-%m-%dT%H:%M:%S")) # Debugging
    # datahora_estimado_datetime = datetime.strptime(datahora_estimado, "%Y-%m-%dT%H:%M:%S") # Testes

    # servico_prestado = 'Saude'
    # origem = 'Cerro Corá'
    # destino = 'Currais Novos'
    # placa = '4N4L1C3'
    # datahora_estimado = datetime(year=2025, month=7, day=4, hour=13, minute=30, second=0)

    # horarioComeco = datetime(year=2025, month=7, day=4, hour=13, minute=30, second=0)
    
    MOCKTrajeto = Trajeto(
        servicoPrestado=servico_prestado,
        pontoOrigem=origem,
        pontoDestino=destino,
        carro_placa=placa,
        horarioEstimado=datahora_estimado.time()
        # motoristaResp=1234567890,      # Descomente se o campo existir no modelo
        # idEmbarcado='abc123'           # Descomente se o campo existir no modelo
    )

    try:
        db.session.add(MOCKTrajeto)
        db.session.commit()
        return jsonify({
            "status": "success",
            "message": "Trajeto inserido com sucesso.",
            "trajeto": {
                "servicoPrestado": MOCKTrajeto.servicoPrestado,
                "pontoOrigem": MOCKTrajeto.pontoOrigem,
                "pontoDestino": MOCKTrajeto.pontoDestino,
                "horarioEstimado": str(MOCKTrajeto.horarioEstimado)
            }
        }), 201
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Erro ao inserir trajeto: {str(e)}"
        }), 400

@view_trajeto.route('/get-all-trajeto', methods=['GET'])
def get_trajeto():
    """
    Rota para exibir todos os trajetos cadastrados.

    Método:
        GET

    Retorno:
        Renderiza o template 'trajetos.html' com todos os trajetos cadastrados.
    """
    trajeto_mostrar = Trajeto.query.all()
    
    return render_template('trajetos.html', all_trajetos=trajeto_mostrar)

@view_trajeto.route('/get-especific-trajeto', methods=['GET'])
def get_especific_trajeto():
    """
    Rota para exibir trajetos específicos com informações de  um motorista específico.

    Método:
        GET

    Retorno:
        Renderiza o template 'trajetos_motorista.html' com trajetos filtrados e dados do motorista.
    """
    cnh_desejado = request.form.get('motorista-cnh')
    motorista_desejado = Motorista.query.filter_by(cnh=cnh_desejado).first()

    if motorista_desejado:
        try:
            trajeto_teste = db.session.query(Trajeto, Motorista).join(Motorista, Trajeto.carro_placa == Motorista.carro_placa).all()
            print(trajeto_teste)
            
        except Exception as e:
            return jsonify({
            "status": "error",
            "message": f"Erro ao inserir trajeto: {str(e)}"
        }), 400

        return render_template('trajetos_motorista.html', especific_trajeto=trajeto_teste), 302
    
    else:
        return jsonify({
                    "status":"error",
                    "message":"motorista nao encontrado"
                    }), 404

@view_trajeto.route('/post-point', methods=['POST'])
def post_ponto_trajeto():
    """
    Rota para postar pontos de um trajeto vindos do embarcado
    
    Método: 
        POST

    Retorno: 
        Nenhum

    OBS: O GET está presente apenas para debug. Necessário retirar
    """

    data = request.get_json() # todos os dados recebidos do embarcado
    latitude_embarcado = data.get('latitude') # latitude passada pelo embarcado
    longitude_embarcado = data.get('longitude') # longitude passada pelo embarcado
    id_trajeto = int(data.get('id-trajeto')) # id do trajeto ao qual o ponto pertence

    # id_trajeto = 1 # mock do id do trajeto ao qual o ponto pertence
    trajeto_desejado = Trajeto.query.filter_by(idTrajeto=id_trajeto).first() # Objeto Trajeto do id correspondente
    # print(trajeto_desejado.trajeto_ponto) # debug

    MOCKPontoTrajeto = PontoTrajeto(
        # latitude='-14.000026', # dado mockado
        # longitude='15.000047', # dado mockado
        latitude=latitude_embarcado,
        longitude=longitude_embarcado,
        trajeto=trajeto_desejado
    )

    try:
        db.session.add(MOCKPontoTrajeto)
        db.session.commit()

        '''
            NÃO POSSUI RETURN
        '''
        return 201

        # return jsonify({
        #     "status": "success",
        #     "message": "Ponto de Trajeto inserido com sucesso.",
        #     "trajeto": {
        #         "latitude": MOCKPontoTrajeto.latitude,
        #         "longitude": MOCKPontoTrajeto.longitude,
        #         "id do trajeto": MOCKPontoTrajeto.trajeto_id,
        #         # "horarioEstimado": str(MOCKTrajeto.horarioEstimado) # caso exista, descomentar
        #     }
        # }), 201
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Erro ao inserir trajeto: {str(e)}"
        }), 400