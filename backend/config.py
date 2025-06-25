from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import create_engine

app = Flask(__name__)

# configurando banco de dados sqlite
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{app.root_path}/database/onebus.db'

# engine = create_engine(f'sqlite:///{app.root_path}/database/onebus.db', pool_size=10, max_overflow=0)

# configurando banco de dados
class Base(DeclarativeBase):
    pass
db = SQLAlchemy(app, model_class=Base)