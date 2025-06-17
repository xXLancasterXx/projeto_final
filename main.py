from flask import Flask, render_template, request
from flask_migrate import Migrate
from utils import db
from usuarios import Usuario
from fichas import Fichas
import os

app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
db_usuario = os.getenv('DB_USERNAME')
db_senha = os.getenv('DB_PASSWORD')
db_host = os.getenv('DB_HOST')
db_mydb = os.getenv('DB_DATABASE')

# conexao = f"mysql+pymysql://{db_usuario}:{db_senha}@{db_host}/{db_mydb}"
conexao = 'sqlite:///db.sqlite3' 

app.config['SQLALCHEMY_DATABASE_URI'] = conexao
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
migrate = Migrate(app, db)

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('nomeUsuario')
        password = request.form.get('password')

        
        if Usuario.query.filter_by(userName=username, password=password).first():
            return render_template('index.html', username=username)

@app.route('/registro')
def registro():
    return render_template('registro.html')

@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('nomeUsuario')
        password = request.form.get('password')
        print(f"Registrando usuário: {username}")
        print(f"Senha: {password}")
        
        if Usuario.query.filter_by(userName=username).first():
            return render_template('registro.html', error='Usuário já existe.')
        else:
            
            user = Usuario(userName=username, password=password)
            db.session.add(user)
            db.session.commit()
            return render_template('login.html')

@app.route('/sobre')
def sobre():
    return render_template('sobre.html')

@app.route('/projetos')
def projetos():
    return render_template('projetos.html')

@app.route('/contato', methods=['GET', 'POST'])
def contato():
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        mensagem = request.form.get('mensagem')
        
        return render_template('contato.html', nome=nome, email=email, mensagem=mensagem)
    return render_template('contato.html')



if __name__ == '__main__':
    app.run(debug=True, port=5000)