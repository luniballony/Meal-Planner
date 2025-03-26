# 🥗 Meal Planner

Projeto Final da Licenciatura em Engenharia Informática (UAb)  
Autores: [Mário Prazeres](mailto:2203127@estudante.uab.pt) & [Matilde Carmo](mailto:2201036@estudante.uab.pt)  
Orientador: Pedro Pestana  
2025

---

## 🔍 Descrição

O **Meal Planner** é uma aplicação web que permite gerar planos semanais de refeições personalizados com base em receitas.  
A plataforma inclui:

- Exploração de receitas com filtros  
- Criação de plano semanal (pequeno-almoço, almoço e jantar)  
- Gestão de utilizadores com login  
- (Futuramente) perfil de utilizador e favoritos

Nesta fase inicial, optou-se por **inserção manual dos dados** para maior controlo e simplicidade.

---

## 🚧 Funcionalidades Implementadas (Back-End)

- Estrutura Flask modular com blueprints (`auth`, `main`)  
- Ligação ao SQL Server local  
- Página de login funcional  
- Verificação de passwords com hash (Werkzeug)  
- Sessão ativa com `session['user_id']`  
- Templates HTML base (login, home)  
- Organização por pastas (`routes/`, `models/`, `templates/`, etc.)

---

## 🧱 Estrutura do Projeto

```plaintext
meal-planner/
├── app/
│   ├── db.py              # Ligação à base de dados
│   ├── models/            # Modelos (user.py, recipe.py)
│   ├── routes/            # Blueprints: auth.py, main.py
│   ├── templates/         # HTML: login, base, home
│   └── __init__.py        # Criação da app Flask
├── config.py              # SECRET_KEY e configs
├── run.py                 # Ficheiro de arranque
├── requirements.txt       # Dependências
└── README.md
```

---

## 💾 Setup do Projeto

### 1. Requisitos

- Python 3.10 ou superior  
- SQL Server instalado localmente  
- ODBC Driver 17 for SQL Server  

### 2. Instalar dependências

```bash
pip install -r requirements.txt
```

### 3. Configurar Base de Dados

- Criar base de dados `meal_planner` no SQL Server.  
- Executar o script `create_tables.sql`.  
- Inserir um utilizador de teste com hash (usar `gerar_hash.py`):

```sql
INSERT INTO utilizadores (nome, email, password_hash)
VALUES ('Matilde', 'matilde@email.com', 'HASH_AQUI');
```

- Confirmar ligação no `db.py` com `Trusted_Connection`.

### 4. Correr a aplicação

```bash
python run.py
```

Depois, aceder a: [http://127.0.0.1:5000/auth/login](http://127.0.0.1:5000/auth/login)

---

## 🧭 Roadmap (Próximos Passos)

- [ ] Registo de utilizadores  
- [ ] Logout e proteção de sessões  
- [ ] Página de receitas  
- [ ] Geração do plano semanal  
- [ ] Design final com Matilde  

---

## 🧰 Tecnologias

- **Back-End**: Flask + Python 3.10  
- **Base de Dados**: SQL Server  
- **Front-End**: HTML + Jinja2 (em desenvolvimento)  
- **Versionamento**: Git + GitHub  
- **Ambiente de trabalho**: VSCode, SSMS  

---

## 🔐 Considerações de Privacidade

- Passwords encriptadas com hashing seguro  
- Apenas email e nome do utilizador são guardados  
- Dados pessoais minimizados e apagáveis a pedido  
=======
