from flask import Flask, render_template, request
from flask import redirect, flash, session
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
            session['user_id'] = Usuario.query.filter_by(userName=username).first().id
            fichas = Fichas.query.filter_by(dono=session['user_id']).all()
            return render_template('index.html', username=username, fichas=fichas)
        else:
            flash('Usuário ou senha inválidos.')
            return redirect('/')

@app.route('/home')
def home():
    user = Usuario.query.get(session.get('user_id'))
    fichas = Fichas.query.filter_by(dono=session.get('user_id')).all()
    nome = user.userName
    return render_template('index.html', fichas=fichas, nome=nome)

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
            flash('Usuário já existe.')
            return redirect('/registro')
        else:
            user = Usuario(userName=username, password=password)
            db.session.add(user)
            db.session.commit()
            flash('Usuário registrado com sucesso!')
            return redirect('/')


@app.route('/criar_ficha', methods=['GET', 'POST'])
def criar_ficha():
    if request.method == 'POST':
        dono = session.get('user_id')  # aqui sim!
        if not dono:
            flash("Você precisa estar logado para criar uma ficha.")
            return redirect('/')
        personagem = request.form['personagem']
        classe = request.form['classe']
        nivel = int(request.form['nivel'])
        raca = request.form['raca']
        forca = int(request.form['forca'])
        destreza = int(request.form['destreza'])
        constituicao = int(request.form['constituicao'])
        inteligencia = int(request.form['inteligencia'])

        nova_ficha = Fichas(
            personagem=personagem,
            dono=dono,
            classe=classe,
            nivel=nivel,
            raca=raca,
            forca=forca,
            destreza=destreza,
            constituicao=constituicao,
            inteligencia=inteligencia
        )

        # Atribuir dono se você usa autenticação
        nova_ficha.dono = session.get('user_id')  # ou o id do usuário logado
        user = Usuario.query.get(nova_ficha.dono)
        nome = user.userName
        db.session.add(nova_ficha)
        db.session.commit()
        flash("Ficha criada com sucesso!")
        return redirect('/home')

    return render_template('criar_ficha.html')

@app.route('/ficha/<int:id>')
def ficha(id):
    ficha = Fichas.query.get_or_404(id)
    return render_template('ficha.html', ficha=ficha)

@app.route('/editar_ficha/<int:id>', methods=['POST'])
def editar_ficha(id):
    ficha = Fichas.query.get_or_404(id)
    
    if request.method == 'POST':
        ficha.classe = request.form['classe']
        ficha.nivel = int(request.form['nivel'])
        ficha.raca = request.form['raca']
        ficha.forca = int(request.form['forca'])
        ficha.destreza = int(request.form['destreza'])
        ficha.constituicao = int(request.form['constituicao'])
        ficha.inteligencia = int(request.form['inteligencia'])

        db.session.commit()
        flash("Ficha editada com sucesso!")
        return redirect(f'/ficha/{id}')

    return render_template('editar_ficha.html', ficha=ficha)

@app.route('/excluir_ficha/<int:id>', methods=['POST'])
def excluir_ficha(id):
    ficha = Fichas.query.get_or_404(id)
    user = Usuario.query.get_or_404(session.get('user_id'))
    nome = user.userName
    
    if request.method == 'POST':
        db.session.delete(ficha)
        db.session.commit()
        flash("Ficha excluída com sucesso!")
        return redirect('/home')

    return render_template('excluir_ficha.html', ficha=ficha)

@app.route('/dados')
def dados():
    return render_template('dados.html')


@app.route('/perfil')
def perfil():
    user = Usuario.query.get_or_404(session.get('user_id'))
    nome = user.userName

    return render_template('perfil.html', nome=nome, user=user)

@app.route('/atualizar_perfil', methods=['POST'])
def atualizar_perfil():
    user = Usuario.query.get_or_404(session.get('user_id'))
    if not user:
        flash("Usuário não encontrado.")
        return redirect('/perfil')

    user.userName = request.form.get('nome')
    db.session.commit()
    flash("Perfil atualizado com sucesso!")
    return redirect('/perfil')

@app.route('/deletar_conta')
def deletar_conta():
    user = Usuario.query.get_or_404(session.get('user_id'))
    if not user:
        flash("Usuário não encontrado.")
        return redirect('/perfil')
    db.session.delete(user)
    db.session.commit()
    flash("Conta deletada com sucesso!")
    session.pop('user_id', None)
    return redirect('/')
if __name__ == '__main__':
    app.run(debug=True, port=5000)