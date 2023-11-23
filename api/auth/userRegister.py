from flask import request, redirect, url_for, render_template, flash
from db.models import User, db
from flask import Blueprint

apiRegisterBlueprint = Blueprint('register', __name__)


@apiRegisterBlueprint.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        new_user = User(username=username)
        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))
    return render_template('register.html')
