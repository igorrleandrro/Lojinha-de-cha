# 🍵 Lojinha de Chá - API de Gestão de Estoque

API RESTful para gerenciamento de estoque, pedidos e clientes de uma loja de chás, desenvolvida com **FastAPI** e **MySQL**. Projeto construído do zero para praticar modelagem de banco de dados, autenticação, regras de negócio e deploy em produção.

🔗 **API publicada:** [lojinha-de-cha.onrender.com/docs](https://lojinha-de-cha.onrender.com/docs)

> ⚠️ A API está hospedada no plano gratuito do Render, que "dorme" após período de inatividade. A primeira requisição pode levar de 30 a 60 segundos para responder.

---

## 📋 Sobre o projeto

O sistema permite gerenciar o catálogo de uma loja de chás (chás, xícaras, ingredientes para boba, bules e acessórios), controlar estoque, cadastrar clientes e registrar pedidos — com baixa automática de estoque e verificação de disponibilidade antes de confirmar uma venda.

### Principais funcionalidades

- **CRUD completo** de categorias, produtos e clientes
- **Pedidos com regra de negócio real**: verificação de estoque antes de criar o pedido, registro do preço no momento da venda, e baixa automática de estoque
- **Autenticação com JWT**: registro e login de usuários, com senhas criptografadas (bcrypt) e endpoints sensíveis protegidos por token
- **Documentação automática interativa** via Swagger UI (`/docs`)

---

## 🛠️ Tecnologias utilizadas

| Camada | Tecnologia |
|---|---|
| Linguagem | Python 3.14 |
| Framework da API | FastAPI |
| Servidor ASGI | Uvicorn |
| ORM | SQLAlchemy |
| Banco de dados | MySQL |
| Autenticação | JWT (python-jose) + bcrypt (passlib) |
| Validação de dados | Pydantic |
| Hospedagem da API | Render |
| Hospedagem do banco | Aiven |

---

## 🗂️ Modelagem do banco de dados

- **Categoria** → agrupa os produtos (ex: Chás, Xícaras e Canecas)
- **Produto** → pertence a uma categoria, tem preço e estoque
- **Cliente** → quem realiza os pedidos
- **Pedido** → associado a um cliente, contém vários itens
- **ItemPedido** → liga produtos a um pedido, guardando quantidade e preço no momento da venda
- **Usuário** → conta de acesso ao sistema (login/senha), separada do Cliente

---

## 🔑 Endpoints principais

| Método | Rota | Descrição | Autenticação |
|---|---|---|---|
| POST | `/registro` | Cria um novo usuário do sistema | Não |
| POST | `/login` | Autentica e retorna um token JWT | Não |
| GET | `/categorias` | Lista todas as categorias | Não |
| POST | `/categorias` | Cria uma nova categoria | Sim |
| GET | `/produtos` | Lista todos os produtos | Não |
| POST | `/produtos` | Cria um novo produto | Sim |
| PUT | `/produtos/{id}` | Atualiza um produto | Sim |
| DELETE | `/produtos/{id}` | Remove um produto | Sim |
| GET | `/clientes` | Lista todos os clientes | Não |
| POST | `/clientes` | Cadastra um novo cliente | Não |
| POST | `/pedidos` | Cria um pedido (com verificação de estoque) | Sim |
| GET | `/pedidos` | Lista todos os pedidos | Não |

A lista completa e testável está disponível na documentação interativa (`/docs`).

---

## 🚀 Como rodar localmente

### Pré-requisitos
- Python 3.11+
- MySQL rodando localmente (ou acesso a um banco remoto)

### Passo a passo

```bash
# Clone o repositório
git clone https://github.com/igorrleandrro/Lojinha-de-cha.git
cd Lojinha-de-cha

# Crie e ative um ambiente virtual
python -m venv .venv
.venv\Scripts\activate      # Windows
source .venv/bin/activate   # Linux/Mac

# Instale as dependências
pip install -r requirements.txt
```

Crie um arquivo `.env` na raiz do projeto com suas credenciais de banco de dados:

```
DB_USER=seu_usuario
DB_PASSWORD=sua_senha
DB_HOST=localhost
DB_PORT=3306
DB_NAME=estoque_db
SECRET_KEY=uma-chave-secreta-qualquer
```

Rode a aplicação:

```bash
uvicorn main:app --reload
```

Acesse a documentação interativa em `http://127.0.0.1:8000/docs`.

---

## 📦 Populando dados de exemplo

O script `seed_dados.py` cadastra automaticamente um conjunto de categorias e produtos de exemplo via API, útil para popular rapidamente um ambiente novo:

```bash
pip install requests
python seed_dados.py
```

---

## 🔮 Possíveis melhorias futuras

- Testes automatizados (pytest)
- Paginação nos endpoints de listagem
- Upload de imagens para os produtos
- Painel administrativo (frontend)
- Relatórios de vendas

---

## 👤 Autor

Desenvolvido por Igor Leandro como projeto de portfólio.
