from flask import Flask
from flask_wtf.csrf import CSRFProtect
from app.db import db
from datetime import datetime, timedelta  # Adicionei timedelta também

# Importar os blueprints
from app.routes.auth import auth_bp
from app.routes.recipes import recipes_bp
from app.routes.meal_plans import meal_plans_bp
from app.routes.admin import admin_bp
from app.routes.main import main_bp
from app.routes.categories import categories_bp

# Instância de proteção CSRF
csrf = CSRFProtect()


def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    csrf.init_app(app)
    db.init_app(app)

    # Registo dos blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(recipes_bp)
    app.register_blueprint(meal_plans_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(categories_bp)

    # Adicionar filtros personalizados para templates
    @app.template_filter("dias_desde")
    def dias_desde(data):
        """Calcula o número de dias desde uma data até hoje."""
        if data:
            return (datetime.utcnow() - data).days
        return 0

    # Adicionar funções globais para templates
    @app.template_global()
    def now():
        """Retorna a data e hora atual."""
        return datetime.now()

    # Adicionar timedelta como global para cálculos de data nos templates
    app.jinja_env.globals["timedelta"] = timedelta

    return app
