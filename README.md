# Meal Planner 🍽️

**Meal Planner** é uma aplicação web desenvolvida no âmbito da Licenciatura em Engenharia Informática (UAb), destinada a ajudar utilizadores a gerir receitas e criar planos semanais de refeições de forma simples, personalizada e eficiente.

## 🚀 Demonstração

- **Versão online**: [web-production-4e3b6.up.railway.app](https://web-production-4e3b6.up.railway.app)
- **Repositório GitHub**: [github.com/luniballony/Meal-Planner](https://github.com/luniballony/Meal-Planner)

---

## 📋 Funcionalidades Principais

- Registo e autenticação segura de utilizadores
- Pesquisa de receitas com filtros (categoria, tempo, etc.)
- Submissão de receitas públicas e privadas
- Criação, edição, visualização e eliminação de planos semanais (pequeno-almoço, almoço, jantar)
- Gestão de receitas favoritas e receitas bloqueadas
- Exportação de planos para PDF (apenas disponível localmente)
- Painel de administração:
  - Aprovação/recusa de receitas submetidas
  - Gestão de utilizadores (bloquear, editar, alterar nível, eliminar)
  - Gestão de categorias (criar, editar, eliminar)
- Diferenciação de perfis: utilizador comum, premium e administrador

---

## 🛠️ Tecnologias Utilizadas

- **Backend:** Python, Flask
- **Frontend:** HTML, CSS, Jinja2
- **Base de Dados:** PostgreSQL (alojada na Railway)
- **ORM:** SQLAlchemy
- **Validação de formulários:** WTForms
- **Segurança:** Werkzeug para hashing seguro de passwords
- **Controlo de versões:** Git & GitHub
- **Ambiente de desenvolvimento:** VS Code
- **Alojamento:** Railway

---

## 📦 Estrutura do Projeto

```shell
Meal-Planner/
├── app/
│   ├── __init__.py
│   ├── db.py
│   ├── models/
│   ├── forms/
│   ├── routes/
│   ├── services/
│   ├── static/
│   └── templates/
├── instance/
│   └── mealplanner.db
├── requirements.txt
├── config.py
├── run.py
├── Procfile
├── .gitignore
└── README.md
```

> Ver estrutura completa e exemplos no relatório/anexos.

---

## ⚙️ Instalação Local

1. **Clonar o repositório:**

   ```bash
   git clone https://github.com/luniballony/Meal-Planner.git
   cd Meal-Planner
   ```

2. **Criar e ativar um ambiente virtual:**

   ```bash
   python -m venv venv
   source venv/bin/activate    # Linux/Mac
   .\venv\Scripts\activate     # Windows
   ```

3. **Instalar as dependências:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar variáveis de ambiente** (criar `.env`):

   ```env
   FLASK_ENV=development
   DATABASE_URL=postgresql://<utilizador>:<senha>@<host>:<porta>/<dbname>
   SECRET_KEY=uma-chave-aleatoria
   ```

5. **Criar e migrar a base de dados:**

   - O projeto já inclui scripts para criação e seed da base de dados.
   - Edita a ligação no `config.py` se necessário.

6. **Correr a aplicação:**
   ```bash
   flask run
   ```

---

## 🧑‍💻 Testes

- Foram implementados **31 testes automáticos** usando `pytest` para validar autenticação, permissões, submissão de receitas, criação/edição de planos, favoritos, bloqueio, etc.
- Para correr os testes:
  ```bash
  pytest
  ```

---

## 📖 Documentação & Relatório

- Toda a informação detalhada sobre o desenho, funcionalidades, código SQL, modelos, manual de utilização e validação está disponível no [Relatório Final - MealPlanner.pdf](link_para_o_relatorio) (anexar PDF ao repositório).
- Inclui diagramas ER, tabelas, exemplos de rotas, modelos SQLAlchemy e templates HTML.

---

## 👥 Autores

- [Mário Prazeres](https://github.com/MPrazeres-1983)
- [Matilde Carmo](https://github.com/luniballony)

Agradecimentos ao Professor Pedro Pestana pelo acompanhamento e sugestões ao longo do projeto.

---

## 📄 Licença

Projeto académico. Uso livre para fins de aprendizagem. Para outros usos, contactar os autores.

---

## 📬 Contacto

Sugestões, bugs ou questões: [Abrir um Issue](https://github.com/luniballony/Meal-Planner/issues) ou contactar via GitHub.

---

> “Planeia a tua semana. Alimenta o teu sucesso!”
