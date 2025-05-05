from flask import Blueprint, render_template, redirect, url_for, flash, session, request
from app.forms.recipe_form import RecipeForm
from app.services.recipe_service import (
    criar_receita,
    listar_receitas,
    obter_receita_por_id,
)
from app.services.category_service import listar_categorias
from collections import defaultdict
from app.forms.favorites_form import AdicionarFavoritoForm


recipes_bp = Blueprint("recipes", __name__, url_prefix="/receitas")


@recipes_bp.route("/submeter", methods=["GET", "POST"])
def submeter():
    if "user_id" not in session:
        flash("Tens de iniciar sessão para submeter receitas.", "warning")
        return redirect(url_for("auth.login"))

    form = RecipeForm()

    # Carregar categorias para o dropdown
    categorias = listar_categorias()
    form.categoria_id.choices = [(c.id, c.nome) for c in categorias]

    if form.validate_on_submit():
        # Modificação aqui: todas as receitas vão para aprovação, independente da opção 'publica'
        dados = {
            "titulo": form.titulo.data,
            "descricao": form.descricao.data,
            "ingredientes": form.ingredientes.data,
            "instrucoes": form.instrucoes.data,
            "tempo_preparacao": form.tempo_preparacao.data,
            "dificuldade": form.dificuldade.data,
            "tags": form.tags.data,
            "categoria_id": form.categoria_id.data,
            "publicada": False,  # Todas as receitas começam como não publicadas
            # Apenas admins (nível 3) podem aprovar diretamente
            "aprovada": True if session.get("user_nivel") == 3 else False,
            "fonte": "utilizador",
        }

        # Guardamos a preferência do usuário para quando o admin aprovar
        publica_quando_aprovada = form.publica.data

        nova_receita = criar_receita(dados, session["user_id"], publica_quando_aprovada)
        flash("Receita submetida com sucesso! Aguarda aprovação.", "success")
        return redirect(url_for("recipes.listar"))

    return render_template("recipes/submeter.html", form=form)


@recipes_bp.route("/", endpoint="listar")
def listar():
    if "user_id" not in session:
        flash("Precisas de iniciar sessão para ver receitas.", "warning")
        return redirect(url_for("auth.login"))

    receitas = listar_receitas()

    # Agrupar receitas por nome da categoria (com fallback se for None)
    agrupadas = defaultdict(list)
    for r in receitas:
        nome_categoria = r.categoria.nome if r.categoria else "Sem categoria"
        agrupadas[nome_categoria].append(r)

    return render_template("recipes/listar.html", receitas_por_categoria=agrupadas)

@recipes_bp.route("/", endpoint="favoritas")
def favoritas():
    return

@recipes_bp.route("/", endpoint="bloqueadas")
def bloqueadas():
    return


@recipes_bp.route("/<int:receita_id>")
def ver(receita_id):
    receita = obter_receita_por_id(receita_id)
    if not receita or (
        not receita.publicada
        and receita.utilizador_id != session.get("user_id")
        and session.get("user_nivel") != 3
    ):
        flash("Receita não encontrada.", "danger")
        return redirect(url_for("recipes.listar"))

    form = AdicionarFavoritoForm()  # <- Adiciona esta linha
    return render_template("recipes/ver.html", receita=receita, form=form)


