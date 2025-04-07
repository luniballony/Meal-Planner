from app.models.meal_plan import MealPlan, MealEntry
from app.db import db
from flask import render_template
import pdfkit
import os


def criar_plano_semanal(utilizador_id, data_inicio, refeicoes_selecionadas):
    plano = MealPlan(utilizador_id=utilizador_id, data_inicio=data_inicio)
    db.session.add(plano)
    db.session.flush()  # Garantir acesso ao plano.id

    for (data_refeicao, refeicao), receita_id in refeicoes_selecionadas.items():
        entrada = MealEntry(
            plano_id=plano.id,
            data_refeicao=data_refeicao,
            refeicao_tipo=refeicao,
            receita_id=receita_id,
        )
        db.session.add(entrada)

    db.session.commit()
    return plano


def atualizar_plano_semanal(plano, nova_data_inicio, refeicoes_selecionadas):
    db.session.query(MealEntry).filter_by(plano_id=plano.id).delete()
    plano.data_inicio = nova_data_inicio

    for (data_refeicao, refeicao), receita_id in refeicoes_selecionadas.items():
        entrada = MealEntry(
            plano_id=plano.id,
            data_refeicao=data_refeicao,
            refeicao_tipo=refeicao,
            receita_id=receita_id,
        )
        db.session.add(entrada)

    db.session.commit()


def obter_planos_do_utilizador(utilizador_id):
    return (
        MealPlan.query.filter_by(utilizador_id=utilizador_id)
        .order_by(MealPlan.data_inicio.desc())
        .all()
    )


def obter_plano_completo(plano_id):
    return MealPlan.query.get(plano_id)


def eliminar_plano(plano_id):
    plano = MealPlan.query.get(plano_id)
    if plano:
        db.session.delete(plano)
        db.session.commit()
        return True
    return False


def exportar_plano_para_pdf(plano):
    # Configuração diferente para Railway vs. desenvolvimento local
    if os.getenv("RAILWAY_ENVIRONMENT"):
        # No Railway, o wkhtmltopdf estará em um caminho diferente
        config = pdfkit.configuration(wkhtmltopdf="/usr/bin/wkhtmltopdf")
    else:
        # Configuração local
        config = pdfkit.configuration(
            wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
        )

    html = render_template("meal_plans/ver_pdf.html", plano=plano)
    options = {
        "enable-local-file-access": None,
        "load-error-handling": "ignore",
        "disable-external-links": None,
    }

    return pdfkit.from_string(html, False, configuration=config, options=options)
