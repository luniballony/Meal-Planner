from flask import Blueprint, session, redirect, url_for, flash, render_template
from app import db
from app.models import Recipe, blocked_recipe
from app.services.blocked_service import desbloquear_receita, listar_nao_bloqueadas, listar_bloqueadas, bloquear_receita
from app.forms.block_recipe_form import BloquearReceitaForm


''' não sei se vamos precisar disto... '''