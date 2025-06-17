from utils import db

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    userName = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def __init__(self, userName, password):
        self.userName = userName
        self.password = password

    def __repr__(self):
        return "<Usuario {}>".format(self.userName)