from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mobile_number = db.Column(db.String(15), unique=True, nullable=False)
    is_verified = db.Column(db.Boolean, default=False)
    balance = db.Column(db.Float, default=0.0)

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player1_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    player2_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='waiting')  # waiting, ongoing, completed
    winner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
