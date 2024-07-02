from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class DueDiligence(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    pdf = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    date_of_submission = db.Column(db.DateTime, nullable=False)

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    question = db.Column(db.Text, nullable=False)
    date_of_submission = db.Column(db.DateTime, nullable=False)
