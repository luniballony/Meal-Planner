from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import check_password_hash
from app.db import get_connection  # 👈 aqui está a ligação

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = get_connection()
        print("Ligação com a BD foi estabelecida com sucesso!")
        cursor = conn.cursor()
        cursor.execute("SELECT id, password_hash FROM utilizadores WHERE email = ?", email)
        user = cursor.fetchone()
        conn.close()

        if user and check_password_hash(user[1], password):
            session['user_id'] = user[0]
            return redirect(url_for('main.home'))
        else:
            flash('Email ou password inválidos')

    return render_template("login.html")
