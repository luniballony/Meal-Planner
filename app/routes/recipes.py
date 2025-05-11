from flask import Blueprint, render_template, redirect, url_for, flash, session
from app.forms.recipe_form import RecipeForm
from app.forms.favorites_form import AdicionarFavoritoForm
from app.forms.block_recipe_form import BloquearReceitaForm
from app.forms.unblock_form import DesbloquearReceitaForm
from app.services.recipe_service import (
    criar_receita,
    listar_receitas,
    obter_receita_por_id,
)
from app.services.category_service import listar_categorias
from app.services.blocked_service import (
    bloquear_receita,
    listar_bloqueadas,
    desbloquear_receita,
    listar_nao_bloqueadas,
)
from collections import defaultdict

recipes_bp = Blueprint("recipes", __name__, url_prefix="/receitas")


@recipes_bp.route("/submeter", methods=["GET", "POST"])
def submeter():
    if "user_id" not in session:
        flash("Tens de iniciar sessão para submeter receitas.", "warning")
        return redirect(url_for("auth.login"))

    form = RecipeForm()
    categorias = listar_categorias()
    form.categoria_id.choices = [(c.id, c.nome) for c in categorias]

    if form.validate_on_submit():
        dados = {
            "titulo": form.titulo.data,
            "descricao": form.descricao.data,
            "ingredientes": form.ingredientes.data,
            "instrucoes": form.instrucoes.data,
            "tempo_preparacao": form.tempo_preparacao.data,
            "dificuldade": form.dificuldade.data,
            "tags": form.tags.data,
            "categoria_id": form.categoria_id.data,
            "publicada": False,
            "aprovada": True if session.get("user_nivel") == 3 else False,
            "fonte": "utilizador",
        }

        publica_quando_aprovada = form.publica.data
        criar_receita(dados, session["user_id"], publica_quando_aprovada)
        flash("Receita submetida com sucesso! Aguarda aprovação.", "success")
        return redirect(url_for("recipes.listar"))

    return render_template("recipes/submeter.html", form=form)


@recipes_bp.route("/", endpoint="listar")
def listar():
    if "user_id" not in session:
        flash("Precisas de iniciar sessão para ver receitas.", "warning")
        return redirect(url_for("auth.login"))

    # user_id = session.get("user_id")
    ''' oculta receitas bloqueadas '''
    receitas = listar_receitas()
    agrupadas = defaultdict(list)
    for r in receitas:
        nome_categoria = r.categoria.nome if r.categoria else "Sem categoria"
        agrupadas[nome_categoria].append(r)

    return render_template("recipes/listar.html", receitas_por_categoria=agrupadas)


@recipes_bp.route("/<int:receita_id>")
def ver(receita_id):
    user_id = session.get("user_id")
    receita = obter_receita_por_id(receita_id)

    # Impede visualizar receita bloqueada
    from app.models import BlockedRecipe

    bloqueada = BlockedRecipe.query.filter_by(
        utilizador_id=user_id, receita_id=receita_id
    ).first()
    if bloqueada:
        '''
        flash("Esta receita está bloqueada.", "warning")
        return redirect(url_for("recipes.listar")) ''' 

        ''' se a receita estiver bloqueada 
                -> remover botão de bloquear a receita 
                -> remover botão de adicionar favoritos
                -> adicionar botão de desbloqueio '''
        pass 
    

    if not receita or (
        not receita.publicada
        and receita.utilizador_id != user_id
        and session.get("user_nivel") != 3
    ):
        flash("Receita não encontrada.", "danger")
        return redirect(url_for("recipes.listar"))

    favorito_form = AdicionarFavoritoForm()
    bloquear_form = BloquearReceitaForm()
    return render_template(
        "recipes/ver.html",
        receita=receita,
        form=favorito_form,
        bloquear_form=bloquear_form,
    )


@recipes_bp.route("/bloquear/<int:receita_id>", methods=["POST"])
def bloquear(receita_id):
    user_id = session.get("user_id")
    if not user_id:
        flash("Precisas de iniciar sessão para bloquear receitas.", "warning")
        return redirect(url_for("auth.login"))

    bloquear_receita(user_id, receita_id)
    flash("Receita bloqueada com sucesso!", "success")
    return redirect(url_for("recipes.listar"))


@recipes_bp.route("/bloqueadas")
def bloqueadas():
    user_id = session.get("user_id")
    if not user_id:
        flash("Precisas de iniciar sessão para ver receitas bloqueadas.", "warning")
        return redirect(url_for("auth.login"))

    receitas = listar_bloqueadas(user_id)
    form = DesbloquearReceitaForm()
    return render_template("recipes/bloqueadas.html", receitas=receitas, form=form)


@recipes_bp.route("/desbloquear/<int:receita_id>", methods=["POST"])
def desbloquear(receita_id):
    user_id = session.get("user_id")
    if not user_id:
        flash("Precisas de iniciar sessão para desbloquear receitas.", "warning")
        return redirect(url_for("auth.login"))

    sucesso = desbloquear_receita(user_id, receita_id)

    if sucesso:
        flash("Receita desbloqueada com sucesso!", "success")
    else:
        flash("A receita não estava bloqueada.", "info")
    return redirect(url_for("recipes.bloqueadas"))


# lista receita individual
@recipes_bp.route("/ver_receita_bloqueada/<int:receita_id>", methods=["GET"])
def ver_receita_bloqueada(receita_id): 
    user_id = session.get("user_id")
    receita = obter_receita_por_id(receita_id)

    if not user_id:
        flash("Precisas de iniciar sessão para ver as tuas receitas bloqueadas.", "warning")
        return redirect(url_for("auth.login"))
    
    if not receita or (
        not receita.publicada
        and receita.utilizador_id != user_id
        and session.get("user_nivel") != 3
    ):
        flash("Receita não encontrada.", "danger")
        return redirect(url_for("recipes.listar"))
    

    unblock_form = DesbloquearReceitaForm()
    return render_template(
        "recipes/ver_bloqueadas.html",
        receita=receita,
        unblock_form=unblock_form
    )
