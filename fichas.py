from utils import db

class Fichas(db.Model):
    __tablename__ = 'fichas'
    id = db.Column(db.Integer, primary_key=True)
    dono = db.Column(
    db.Integer,
    db.ForeignKey('usuarios.id', name='fk_fichas_dono'),
    nullable=False
    )
    personagem = db.Column(db.String(80), nullable=False)
    classe = db.Column(db.String(80), nullable=False)
    nivel = db.Column(db.Integer, nullable=False)
    raca = db.Column(db.String(80), nullable=False)
    forca = db.Column(db.Integer, nullable=False)
    destreza = db.Column(db.Integer, nullable=False)
    constituicao = db.Column(db.Integer, nullable=False)
    inteligencia = db.Column(db.Integer, nullable=False)

    def __init__(self, personagem, dono, classe, nivel, raca, forca, destreza, constituicao, inteligencia):
        self.personagem = personagem
        self.dono = dono
        self.classe = classe
        self.nivel = nivel
        self.raca = raca
        self.forca = forca
        self.destreza = destreza
        self.constituicao = constituicao
        self.inteligencia = inteligencia