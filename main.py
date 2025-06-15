from flask import Flask, render_template, request
from flask_migrate import Migrate
from database import db
from usuarios import Usuario
from fichas import Fichas

app = Flask(__name__)

app.config['SECRET_KEY'] = 'elegebete'
conexao = 'sqlite:///banco.db'
app.config['SQLALCHEMY_DATABASE_URI'] = conexao
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
migrate = Migrate(app, db)

@app.route('/')
def index():
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