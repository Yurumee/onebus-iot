from config import db, app
from flask import Blueprint, jsonify, render_template

view_index = Blueprint('view_index', __name__)

@view_index.route('/', methods=['GET'])
def index():
    """
    Rota principal da API.

    Método:
        GET

    Retorno:
        Página index do sistema ONEBUS (para teste).
    """
    return render_template('index.html')