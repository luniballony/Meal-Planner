from flask import Blueprint, render_template, session, redirect, url_for, flash

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def home():
    if "user_id" not in session:
        flash("Precisas de iniciar sessão para aceder ao Meal Planner.", "warning")
        return redirect(url_for("auth.login"))

    return render_template(
        "main/home.html", nome=session.get("user_nome", "Utilizador")
    )
