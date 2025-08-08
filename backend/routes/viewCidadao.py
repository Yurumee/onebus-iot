from config import db
from flask import Blueprint, request, jsonify, render_template
from models.cidadao import Cidadao
from models.trajetos_cidadaos import TrajetosCidadaos
from models.trajeto  import Trajeto

view_cidadao = Blueprint('view_cidadao', __name__)

@view_cidadao.route('/', methods=['GET', 'POST'])
def post_new_cidadao():
    """
    Rota para cadastrar um cidadão no banco de dados.

    Método:
        GET, POST
        get: exibir pagina
        post: cadastro dos dados

    Retorno:
        - status, message e dados do cidadão.
        - status error se o cidadão já existe.
    """
    if request.method == 'POST':

        data = request.get_json()
        cpf_cidadao = data.get('cidadao-cpf')
        nome_cidadao = data.get('cidadao-nome')
        senha = data.get('senha')

        # cpf = '789.456.123-00'
        # nome = 'Alice Mock'
        # senha = 'senhaforte123'
        try:
            cidadao = Cidadao.query.filter_by(cpf=cpf_cidadao).first()
        except Exception as e:
            return jsonify({
                "status":"error",
                "message":f"{str(e)}"
            }), 400

        if cidadao:
            return jsonify({
                "status": "error",
                "message": "Cidadão já cadastrado.",
                "cpf": cpf_cidadao,
                "nome": cidadao.nome_completo
            }), 409

        new_cidadao = Cidadao(
            cpf=cpf_cidadao,
            nome_completo=nome_cidadao,
            senha=senha,
            tipo_usuario='cidadao'
        )

        db.session.add(new_cidadao)
        db.session.commit()

        return jsonify({
            "status": "success",
            "message": "Cidadão cadastrado com sucesso.",
            "cpf": cpf_cidadao,
            "nome": nome_cidadao
        }), 201
    
    return render_template('pagina_cadastro.html'), 302
    # return jsonify({
    #     'status':'OK'
    # })

@view_cidadao.route('/todos', methods=['GET'])
def get_cidadao():
    """
    Rota para mostrar todos os cidadaos

    Método:
        Get

    Retorno:
        Página listando todos os cidadaos
    """
        
    cidadaos = Cidadao.query.all()

    return render_template('todos-cidadaos.html', all_cidadao=cidadaos), 302

@view_cidadao.route('/cidadao-especifico', methods=['GET'])
def get_especific_cidadao():
    """
    Rota para mostrar um cidadao especifico pelo cpf informada

    Método:
        Get

    Retorno:
        Página listando cidadao especifico
    """

    data = request.get_json()
    cpf_desejado = data.get('cidadao-cpf')
    
    try:
        cidadao = Cidadao.query.filter_by(cpf=cpf_desejado).first()
    except Exception as e:
        return jsonify({
            'status':'error',
            'message':f'{str(e)}'
        }), 400

    if cidadao:
        return render_template('cidadao_especifico.html', cidadao=cidadao), 302
    else:
        return jsonify({
            'status':'error',
            'message':f'cidadao não encontrado: {str(e)}'
        }), 404

@view_cidadao.route('/trajetos', methods=['GET'])
def get_trajetos_vinculados():
    """
    Rota para mostrar os trajetos de um cidadao especifico

    Método:
        Get

    Retorno:
        Página listando os trajetos do cidadao
    """
    data = request.get_json()
    cpf_desejado = data.get('cidadao-cpf')
    cidadao = Cidadao.query.filter_by(cpf=cpf_desejado).first()
    if cidadao:
        # trajetos_cidadao = TrajetosCidadaos.query.filter_by(cidadao_cpf=cpf_desejado).all()
        trajetos_cidadao = db.session.query(TrajetosCidadaos, Trajeto).join(Trajeto, (Trajeto.id_trajeto == TrajetosCidadaos.trajeto_id) & (TrajetosCidadaos.cidadao_cpf == cpf_desejado)).all()
        """DEBUG"""
        # print(f'trajetos: {trajetos_cidadao}')
        # print(f'retorno do trajeto 1 (id do trajeto): {trajetos_cidadao[0][0].trajeto_id}')
        # print(f'retorno do trajeto 1 (placa): {trajetos_cidadao[0][1].carro_placa}')
        # print(f'retorno do trajeto 1 (origem): {trajetos_cidadao[0][1].ponto_origem}')
        # print(f'retorno do trajeto 1 (destino): {trajetos_cidadao[0][1].ponto_destino}')
        # print(f'retorno do trajeto 1 (horario): {trajetos_cidadao[0][1].horario_estimado}')
        
        # print(f'objeto trajeto no index [1]: {trajetos_cidadao[1]}')
        
        # print(f'retorno do trajeto 3 (id do trajeto): {trajetos_cidadao[1][0].trajeto_id}')
        # print(f'retorno do trajeto 3 (placa): {trajetos_cidadao[1][1].carro_placa}')
        # print(f'retorno do trajeto 3 (origem): {trajetos_cidadao[1][1].ponto_origem}')
        # print(f'retorno do trajeto 3 (destino): {trajetos_cidadao[1][1].ponto_destino}')
        # print(f'retorno do trajeto 3 (horario): {trajetos_cidadao[1][1].horario_estimado}')
        
        resposta_json = {}
        for trajeto in trajetos_cidadao:
            resposta_json[trajeto[0].trajeto_id] = {"trajeto_id": trajeto[0].trajeto_id, "carro_placa": trajeto[1].carro_placa, "ponto_origem": trajeto[1].ponto_origem, "ponto_destino": trajeto[1].ponto_destino, "horario_estimado": str(trajeto[1].horario_estimado)}

        return jsonify({
            "status": "success",
            "message": "Trajetos encontrados.",
            "trajetos": resposta_json,
        }), 200
    else:
        return jsonify({
            'status':'error',
            'message':f'cidadao não encontrado'
        }), 404


@view_cidadao.route('/alterar-cidadao', methods=['GET', 'PATCH'])
def edit_cidadao():
    """
    Rota para editar um cidadão.

    Métodos:
        GET, PATCH

    Parâmetros esperados (via formulário):
        - cpf: cpf do cidadão a ser alterado
        - nome: novo nome do cidadão

    Retorno:
        - status, message e dados do cidadão.
        - status error se usuário não existir ou senha estiver incorreta.
    """

    if request.method == 'PATCH':

        data = request.get_json()
        cpf_cidadao = data.get('cidadao-cpf')

        try:
            cidadao = Cidadao.query.filter_by(cpf=cpf_cidadao).first()
        except Exception as e:
            return jsonify({
                "status":"error",
                "message":f"{str(e)}"
            })
        
        if cidadao:
            new_nome = data.get('cidadao-nome')

            if new_nome != cidadao.nome_completo:
                try:
                    cidadao.nome_completo = new_nome
                    db.session.commit()

                except Exception as e:
                    return jsonify({
                        "status":"error",
                        "message":f"{str(e)}"
                    })
                
                return jsonify({
                    "status":"success",
                    "message":"update realizado com sucesso"
                }), 200
            
            else:
                return jsonify({
                    "status":"error",
                    "message":"o nome precisa ser diferente do atual"
                }), 400
        else:
            return jsonify({
                "status":"error",
                "message":"cidadao nao encontrado"
            }), 404
        
    return render_template('pagina_editar_cidadao.html'), 302
            

@view_cidadao.route('/excluir-cidadao', methods=['GET', 'DELETE'])
def delete_cidadao():
    """
    Rota para deletar um cidadão.

    Métodos:
        GET, DELETE

    Parâmetros esperados:
        - cpf: cpf do cidadão

    Retorno:
        - status, message.
        - status error se usuário não existir
    """

    if request.method == 'DELETE':
        data = request.get_json()
        cpf_cidadao = data.get('cidadao-cpf')

        try:
            cidadao = Cidadao.query.filter_by(cpf=cpf_cidadao).first()
        except Exception as e:
            return jsonify({
                "status":"error",
                "message":f"{str(e)}"
            }), 400
        
        if cidadao:
            try:
                Cidadao.query.filter_by(cpf=cpf_cidadao).delete()
                db.session.commit()
                return jsonify({
                    "status":"success",
                    "message":"cidadao deletado"
                }), 204
            
            except Exception as e:
                return jsonify({
                "status":"error",
                "message":f"{str(e)}"
            }), 400

        else:
            return jsonify({
                "status":"error",
                "message":"cidadao nao encontrado"
            }), 404
    
    return render_template('pagina_deletar_cidadao.html'), 302
        

@view_cidadao.route('/login', methods=['GET', 'POST'])
def login():
    """
    Rota para autenticação de cidadão.

    Métodos:
        GET, POST

    Parâmetros esperados (via formulário):
        - cpf: cpf do cidadão
        - senha: Senha do cidadão

    Retorno:
        - status, message e dados do cidadão.
        - status error se usuário não existir ou senha estiver incorreta.
    """

    if request.method == 'POST':
    
        dadosRequest = request.get_json()
        cpf = dadosRequest.get('cpf')
        password = dadosRequest.get('senha')

        user = Cidadao.query.filter_by(cpf=cpf).first()

        if user:
            if user.senha == password:
                return jsonify({
                    "status": "success",
                    "message": "Autenticação realizada com sucesso.",
                    "cpf": cpf,
                    "nome": user.nome_completo
                }), 200
            
            else:
                return jsonify({
                    "status": "error",
                    "message": "Senha incorreta.",
                    "cpf": cpf
                }), 401

        return jsonify({
            "status": "error",
            "message": "Usuário não encontrado.",
            "cpf": cpf
        }), 404

    return render_template('pagina_login.html'), 302