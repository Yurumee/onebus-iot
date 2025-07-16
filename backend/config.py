from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
# from sqlalchemy import create_engine

app = Flask(__name__, template_folder='../frontend/templates')

# configurando banco de dados sqlite
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{app.root_path}/database/onebus.db'

# engine = create_engine(f'sqlite:///{app.root_path}/database/onebus.db', pool_size=10, max_overflow=0)

# configurando banco de dados
class Base(DeclarativeBase):
    # responsáveis para relacionamento 1:N
    __abstract__ = True
    __allow_unmapped__ = True

db = SQLAlchemy(app, model_class=Base)