"""
Script para popular a API da Lojinha de Chá com dados de exemplo.
Roda contra a API publicada (Render), usando a biblioteca 'requests'.

Como usar:
1. Ajuste a variável BASE_URL se necessário.
2. Ajuste EMAIL e SENHA para um usuário que já exista (ou deixe como está
   para criar um novo usuário automaticamente).
3. Rode: python seed_dados.py
"""

import requests

BASE_URL = "https://lojinha-de-cha.onrender.com"

EMAIL = "admin@lojinha.com"
SENHA = "admin12345"
NOME = "Admin"

CATEGORIAS = [
    "Chás",
    "Xícaras e Canecas",
    "Ingredientes para Boba",
    "Bules e Chaleiras",
    "Acessórios",
]

# (nome, descricao, preco, quantidade_estoque, nome_da_categoria)
PRODUTOS = [
    ("Chá Verde Jasmim", "Chá verde com flores de jasmim", 24.90, 50, "Chás"),
    ("Chá Preto Earl Grey", "Chá preto aromatizado com bergamota", 22.90, 40, "Chás"),
    ("Chá de Camomila", "Chá calmante de camomila pura", 18.90, 35, "Chás"),
    ("Chá Branco Pêssego", "Chá branco suave com sabor de pêssego", 26.90, 30, "Chás"),
    ("Chá Chai Especiado", "Mistura de especiarias indianas com chá preto", 27.90, 25, "Chás"),
    ("Xícara de Porcelana Branca", "Xícara clássica de porcelana, 200ml", 34.90, 20, "Xícaras e Canecas"),
    ("Caneca Térmica com Tampa", "Caneca térmica de aço inox, mantém a temperatura", 49.90, 15, "Xícaras e Canecas"),
    ("Xícara Japonesa sem Alça", "Xícara estilo tradicional japonês", 29.90, 18, "Xícaras e Canecas"),
    ("Bolinhas de Tapioca (Boba)", "Pacote de bolinhas de tapioca para bubble tea", 15.90, 60, "Ingredientes para Boba"),
    ("Xarope de Taro", "Xarope concentrado sabor taro", 19.90, 25, "Ingredientes para Boba"),
    ("Xarope de Morango", "Xarope concentrado sabor morango", 17.90, 30, "Ingredientes para Boba"),
    ("Pérolas de Fruta Explosivas", "Pérolas que explodem sabor na boca", 21.90, 20, "Ingredientes para Boba"),
    ("Bule de Sakura", "Bule para chá com decorações de sakura estilo japonês", 59.90, 15, "Bules e Chaleiras"),
    ("Chaleira Amarela", "Chaleira amarela com tampa", 59.90, 12, "Bules e Chaleiras"),
    ("Bule de Vidro Resistente", "Bule de vidro borossilicato, vai ao fogo", 44.90, 18, "Bules e Chaleiras"),
    ("Infusor de Aço Inox", "Infusor de aço inox fácil de lavar", 9.90, 40, "Acessórios"),
    ("Canudo de Metal para Boba", "Canudo largo reutilizável de aço inox", 12.90, 30, "Acessórios"),
    ("Coador de Chá de Bambu", "Coador artesanal de bambu", 14.90, 22, "Acessórios"),
]


def registrar_ou_logar():
    print("Tentando registrar usuário...")
    resp = requests.post(
        f"{BASE_URL}/registro",
        json={"nome": NOME, "email": EMAIL, "senha": SENHA},
    )
    if resp.status_code == 200:
        print("Usuário criado com sucesso.")
    elif resp.status_code == 400:
        print("Usuário já existia, seguindo para login.")
    else:
        print("Aviso ao registrar:", resp.status_code, resp.text)

    print("Fazendo login...")
    resp = requests.post(
        f"{BASE_URL}/login",
        json={"email": EMAIL, "senha": SENHA},
    )
    resp.raise_for_status()
    token = resp.json()["access_token"]
    print("Login OK, token obtido.")
    return token


def criar_categorias(token):
    headers = {"Authorization": f"Bearer {token}"}
    nome_para_id = {}

    # Evita duplicar categorias já existentes
    existentes = requests.get(f"{BASE_URL}/categorias").json()
    for c in existentes:
        nome_para_id[c["nome"]] = c["id"]

    for nome in CATEGORIAS:
        if nome in nome_para_id:
            print(f"Categoria '{nome}' já existe (id {nome_para_id[nome]}), pulando.")
            continue
        resp = requests.post(f"{BASE_URL}/categorias", json={"nome": nome}, headers=headers)
        if resp.status_code == 200:
            dados = resp.json()
            nome_para_id[nome] = dados["id"]
            print(f"Categoria criada: {nome} (id {dados['id']})")
        else:
            print(f"Erro ao criar categoria '{nome}':", resp.status_code, resp.text)

    return nome_para_id


def criar_produtos(token, nome_para_id):
    headers = {"Authorization": f"Bearer {token}"}

    for nome, descricao, preco, estoque, categoria_nome in PRODUTOS:
        categoria_id = nome_para_id.get(categoria_nome)
        if categoria_id is None:
            print(f"Categoria '{categoria_nome}' não encontrada, pulando produto '{nome}'.")
            continue

        payload = {
            "nome": nome,
            "descricao": descricao,
            "preco": preco,
            "quantidade_estoque": estoque,
            "categoria_id": categoria_id,
        }
        resp = requests.post(f"{BASE_URL}/produtos", json=payload, headers=headers)
        if resp.status_code == 200:
            print(f"Produto criado: {nome}")
        else:
            print(f"Erro ao criar produto '{nome}':", resp.status_code, resp.text)


if __name__ == "__main__":
    token = registrar_ou_logar()
    nome_para_id = criar_categorias(token)
    criar_produtos(token, nome_para_id)
    print("\nConcluído! Confira em:", f"{BASE_URL}/produtos")
