# from api.auth import userRegister  # Importieren der Auth-Routen
from db.models import User  # Importieren Sie das User-Modell
from api.extractImg2Text import apiBlueprint
from flask import Flask, render_template, request, redirect, url_for, flash
from db.db import db


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SECRET_KEY'] = 'passwortxyz123'

db.init_app(app)
with app.app_context():
    db.create_all()  # Erstellen der Datenbanktabellen


# Importieren Sie Ihren Blueprint nach der Initialisierung der App
app.register_blueprint(apiBlueprint, url_prefix='/api')


@app.route('/')
def index():
    return redirect(url_for('home'))


@app.route('/home')
def home():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Dieser Benutzername ist bereits vergeben.')
            return redirect(url_for('register'))

        new_user = User(username=username)
        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        if user is not None and user.check_password(password):
            # Hier können Sie die Benutzersitzung einrichten
            # Leitet zu einer anderen Seite um, z.B. die Startseite
            return redirect(url_for('home'))
        else:
            flash('Ungültiger Benutzername oder Passwort!')

    return render_template('login.html')


if __name__ == '__main__':
    app.run(debug=True)
