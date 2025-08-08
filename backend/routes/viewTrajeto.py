from config import db
from flask import Blueprint, jsonify, render_template, request
from datetime import datetime
from models.trajeto import Trajeto
from models.pontoTrajeto import PontoTrajeto
from models.trajetos_cidadaos import TrajetosCidadaos
from models.motorista import Motorista
from models.carro import Carro
from models.cidadao import Cidadao

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
    if request.method == 'POST':
        data = request.get_json()
        servico_prestado = data.get('servico-prestado')
        origem = data.get('origem')
        destino = data.get('destino')
        placa = data.get('placa')
        datahora_estimado = datetime.strptime(data.get('datahora-estimado'), "%Y-%m-%dT%H:%M:%S")
        # print("datahora_estimado (datetime)=", datetime.strptime(datahora_estimado, "%Y-%m-%dT%H:%M:%S")) # Debugging

        # servico_prestado = 'Saude'
        # origem = 'Cerro Corá'
        # destino = 'Currais Novos'
        # placa = '4N4L1C3'
        # datahora_estimado = datetime(year=2025, month=7, day=4, hour=13, minute=30, second=0)

        # horarioComeco = datetime(year=2025, month=7, day=4, hour=13, minute=30, second=0)

        new_trajeto = Trajeto(
            servico_prestado=servico_prestado,
            ponto_origem=origem,
            ponto_destino=destino,
            # carro_placa=placa,
            horario_estimado=datahora_estimado.time()
            # motoristaResp=1234567890,      # Descomente se o campo existir no modelo
            # idEmbarcado='abc123'           # Descomente se o campo existir no modelo
        )
    
        carro_desejado = Carro.query.filter_by(placa=placa).first()
        carro_desejado.trajeto.append(new_trajeto)

        try:
            db.session.add(new_trajeto)
            db.session.commit()
            return jsonify({
                "status": "success",
                "message": "Trajeto inserido com sucesso.",
                "trajeto": {
                    "servico_prestado": new_trajeto.servico_prestado,
                    "ponto_origem": new_trajeto.ponto_origem,
                    "ponto_destino": new_trajeto.ponto_destino,
                    "horario_estimado": str(new_trajeto.horario_estimado)
                }
            }), 201
        
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": f"Erro ao inserir trajeto: {str(e)}"
            }), 400
    
    return render_template('pagina_cadastrar_projeto.html'), 302

@view_trajeto.route('/alterar-trajeto', methods=['GET', 'PATCH'])
def edit_trajeto():
    """
    Rota para editar um trajeto específico com o id informado

    Método:
        Get, Patch

    Retorno:
        Página mostrando trajeto editado
    """

    if request.method == 'PATCH':
        data = request.get_json()
        trajeto_id = data.get('id-trajeto')
        
        try:
            trajeto_desejado = Trajeto.query.filter_by(id_trajeto=trajeto_id).first()
        
        except Exception as e:
            return jsonify({
                "status":"error",
                "message":f"houve um erro ao tentar pesquisar o trajeto no banco de dados: {str(e)}"
            }), 400

        if trajeto_desejado:
            new_servico = data.get('servico-prestado')
            new_ponto_origem = data.get('ponto-origem')
            new_ponto_destino = data.get('ponto-destino')
            new_horario = data.get('horario-estimado')
            new_placa = data.get('placa-carro')

            if new_servico != trajeto_desejado.servico_prestado and new_servico != None:
                
                trajeto_desejado.servico_prestado = new_servico
                db.session.commit()
            
            if new_ponto_origem != trajeto_desejado.ponto_origem and new_ponto_origem != None:
                
                trajeto_desejado.ponto_origem = new_ponto_origem
                db.session.commit()
            
            if new_ponto_destino != trajeto_desejado.ponto_destino and new_ponto_destino != None:
                
                trajeto_desejado.ponto_destino = new_ponto_destino
                db.session.commit()

            if new_horario != trajeto_desejado.horario_estimado and new_horario != None:
                
                trajeto_desejado.horario_estimado = new_horario
                db.session.commit()

            if new_placa != trajeto_desejado.carro_placa and new_placa != None:
                carro_desejado = Carro.query.filter_by(placa=new_placa).first()

                if carro_desejado:
                    carro_desejado.trajeto.append(trajeto_desejado)
                    db.session.commit()

                else:
                    return jsonify({
                        "status":"not found",
                        "message":"carro nao existe"
                    }), 404

            return jsonify({
                "status":"success",
                "message":"update realizado com sucesso"
            }), 200

        else:
            return jsonify({
                "status":"not found",
                "message":"o trajeto não existe"
            }), 404
    
    return render_template('pagina_editar_trajeto.html'), 302

@view_trajeto.route('/excluir-trajeto', methods=['GET','DELETE'])
def delete_trajeto():
    if request.method == 'DELETE':
        
        data = request.get_json()
        trajeto_id = data.get('id-trajeto')

        try:
            trajeto_desejado = Trajeto.query.filter_by(id_trajeto=trajeto_id).first()
        except Exception as e:
            return jsonify({
                "status":"error",
                "message":f"{str(e)}"
            })
        
        if trajeto_desejado:
            db.session.query(TrajetosCidadaos).where(TrajetosCidadaos.trajeto_id == trajeto_desejado.id_trajeto).delete()
            Trajeto.query.filter_by(id_trajeto=trajeto_id).delete()

            db.session.commit()
            return jsonify({
                "status":"success",
                "message":"trajeto deletado com sucesso"
            })

        else:
            return jsonify({
                "status":"not found",
                "message":"o trajeto nao existe"
            })

    else:
        return render_template('pagina_deletar_trajeto.html')

@view_trajeto.route('/todos', methods=['GET'])
def get_trajeto():
    """
    Rota para exibir todos os trajetos cadastrados.

    Método:
        GET

    Retorno:
        Renderiza o template 'trajetos.html' com todos os trajetos cadastrados.
    """
    trajeto_mostrar = Trajeto.query.all()
    
    return render_template('trajetos.html', all_trajetos=trajeto_mostrar), 302

@view_trajeto.route('/rota-motorista', methods=['GET'])
def get_especific_trajeto():
    """
    Rota para exibir trajetos específicos com informações de  um motorista específico.

    Método:
        GET

    Retorno:
        Renderiza o template 'trajetos_motorista.html' com trajetos filtrados e dados do motorista.
    """
    data = request.get_json()
    cnh_desejado = data.get('motorista-cnh')
    motorista_desejado = Motorista.query.filter_by(cnh=cnh_desejado).first()

    if motorista_desejado:
        try:
            trajeto_teste = db.session.query(Trajeto, Motorista).join(Motorista, Trajeto.carro_placa == Motorista.carro_placa).all()
            # print(trajeto_teste)
            
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


@view_trajeto.route('/vincular-cidadao', methods=['GET', 'POST'])
def register_cidadao():
    """
    Rota para vincular um cidadao específico a um trajeto especifico.

    Método:
        GET, POST

    Retorno:
        Renderiza o template 'trajeto-cidadao.html' com o trajeto do cidadao desejado.
    """

    if request.method == 'POST':
        data = request.get_json()
        cpf_desejado = data.get('cidadao-cpf')
        trajeto_id = data.get('id-trajeto')

        # print(f'teste de cpf: {cpf_desejado}')

        trajeto_desejado = Trajeto.query.filter_by(id_trajeto=trajeto_id).first()
        cidadao_desejado = Cidadao.query.filter_by(cpf=cpf_desejado).first()
        
        # print(f'teste de cpf: {cidadao_desejado}')
        # print(f'teste de trajeto: {trajeto_desejado}')

        if cidadao_desejado == None or trajeto_desejado == None:
            return jsonify({
                'status':'not found',
                'message':'cidadao ou trajeto nao encontrado'
            }), 404
        
        else:
            print(f'teste do if: {TrajetosCidadaos.query.filter(TrajetosCidadaos.cidadao_cpf==cpf_desejado, TrajetosCidadaos.trajeto_id==trajeto_id).first()}')

            if TrajetosCidadaos.query.filter(TrajetosCidadaos.cidadao_cpf==cpf_desejado, TrajetosCidadaos.trajeto_id==trajeto_id).first():
                return jsonify({
                    'status':'error',
                    'message':'cidadao já vinculado a esse trajeto'
                }), 400
            
            else:
                try:
                    trajeto_vinculado = TrajetosCidadaos(
                        cidadao=cidadao_desejado,
                        trajeto=trajeto_desejado
                    )

                    db.session.add(trajeto_vinculado)
                    db.session.commit()
                    
                    # return render_template('pagina_vincular_cidadao.html'), 302
                    return jsonify({
                        'status':'success',
                        'message':'cidadao vinculado ao trajeto'
                    }), 201
                
                except Exception as e:
                    return jsonify({
                        'status':'error',
                        'message':f'{str(e)}'
                    }), 400

    
    return render_template('pagina_vincular_cidadao.html'), 302

@view_trajeto.route('/desvincular-cidadao', methods=['GET', 'POST'])
def delete_vinculo_cidadao():
    
    if request.method == 'POST':
        data = request.get_json()
        cpf_cidadao = data.get('cidadao-cpf')
        trajeto_id = data.get('id-trajeto')

        vinculo_desejado = TrajetosCidadaos.query.filter(TrajetosCidadaos.cidadao_cpf==cpf_cidadao, TrajetosCidadaos.trajeto_id==trajeto_id).first()

        # print(f'vinculo: {vinculo_desejado}')

        if vinculo_desejado:
            TrajetosCidadaos.query.filter(TrajetosCidadaos.cidadao_cpf==cpf_cidadao, TrajetosCidadaos.trajeto_id==trajeto_id).delete()
            db.session.commit()

            return jsonify({
                'status':'deleted',
                'message':'vinculo deletado com sucesso'
            })
        
        else:
            return jsonify({
                'status':'not fuound',
                'message':'vinculo nao existe'
            })

    return render_template('pagina_deletar_vinculo.html'), 302

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
    trajeto_desejado = Trajeto.query.filter_by(id_trajeto=id_trajeto).first() # Objeto Trajeto do id correspondente
    # print(trajeto_desejado.trajeto_ponto) # debug

    new_ponto = PontoTrajeto(
        # latitude='-14.000026', # dado mockado
        # longitude='15.000047', # dado mockado
        latitude=latitude_embarcado,
        longitude=longitude_embarcado,
        trajeto=trajeto_desejado
    )

    try:
        db.session.add(new_ponto)
        db.session.commit()

        '''
            NÃO POSSUI RETURN
        '''
        return 201
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Erro ao inserir trajeto: {str(e)}"
        }), 400