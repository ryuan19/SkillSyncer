from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(80), nullable=False)

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(100))
    summary = db.Column(db.Text, nullable=False)
    skills = db.Column(db.Text, nullable=False)
    hobbies = db.Column(db.Text, nullable=False)
    jobs = db.Column(db.Text, nullable=False)
    embedding_list = db.Column(db.Text, nullable=False)
    user = db.relationship('User', backref=db.backref('employees', lazy=True))


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    embedding_text = db.Column(db.Text, nullable=False)
    best_employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'))
    best_employee_name = db.Column(db.String(100))
    best_employee_reason = db.Column(db.Text, nullable=False)
    user = db.relationship('User', backref=db.backref('projects', lazy=True))
