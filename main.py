from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db, engine, Base
import models
import schemas
import auth

# Cria as tabelas no banco (se ainda não existirem) com base nos models
Base.metadata.create_all(bind=engine)

app = FastAPI(title="API de Estoque")


@app.get("/")
def home():
    return {"status": "API rodando"}


# Criar uma categoria
@app.post("/categorias", response_model=schemas.CategoriaResponse)
def criar_categoria(categoria: schemas.CategoriaCreate, db: Session = Depends(get_db)):
    nova_categoria = models.Categoria(nome=categoria.nome)
    db.add(nova_categoria)
    db.commit()
    db.refresh(nova_categoria)
    return nova_categoria


# Listar todas as categorias
@app.get("/categorias", response_model=list[schemas.CategoriaResponse])
def listar_categorias(db: Session = Depends(get_db)):
    return db.query(models.Categoria).all()


# Buscar uma categoria específica pelo id
@app.get("/categorias/{categoria_id}", response_model=schemas.CategoriaResponse)
def buscar_categoria(categoria_id: int, db: Session = Depends(get_db)):
    categoria = db.query(models.Categoria).filter(models.Categoria.id == categoria_id).first()
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    return categoria


# Deletar uma categoria
@app.delete("/categorias/{categoria_id}")
def deletar_categoria(categoria_id: int, db: Session = Depends(get_db)):
    categoria = db.query(models.Categoria).filter(models.Categoria.id == categoria_id).first()
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    db.delete(categoria)
    db.commit()
    return {"mensagem": "Categoria deletada com sucesso"}

@app.post("/produtos", response_model=schemas.ProdutoResponse)
def criar_produto(produto: schemas.ProdutoCreate, db: Session = Depends(get_db)):
    novo_produto = models.Produto(**produto.model_dump())
    db.add(novo_produto)
    db.commit()
    db.refresh(novo_produto)
    return novo_produto


# Listar todos os produtos
@app.get("/produtos", response_model=list[schemas.ProdutoResponse])
def listar_produtos(db: Session = Depends(get_db)):
    return db.query(models.Produto).all()


# Buscar um produto específico
@app.get("/produtos/{produto_id}", response_model=schemas.ProdutoResponse)
def buscar_produto(produto_id: int, db: Session = Depends(get_db)):
    produto = db.query(models.Produto).filter(models.Produto.id == produto_id).first()
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return produto


# Atualizar um produto (ex: mudar preço ou estoque)
@app.put("/produtos/{produto_id}", response_model=schemas.ProdutoResponse)
def atualizar_produto(produto_id: int, dados: schemas.ProdutoCreate, db: Session = Depends(get_db)):
    produto = db.query(models.Produto).filter(models.Produto.id == produto_id).first()
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    for campo, valor in dados.model_dump().items():
        setattr(produto, campo, valor)
    db.commit()
    db.refresh(produto)
    return produto


# Deletar um produto
@app.delete("/produtos/{produto_id}")
def deletar_produto(produto_id: int, db: Session = Depends(get_db)):
    produto = db.query(models.Produto).filter(models.Produto.id == produto_id).first()
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    db.delete(produto)
    db.commit()
    return {"mensagem": "Produto deletado com sucesso"}

# Criar um cliente
@app.post("/clientes", response_model=schemas.ClienteResponse)
def criar_cliente(cliente: schemas.ClienteCreate, db: Session = Depends(get_db)):
    novo_cliente = models.Cliente(**cliente.model_dump())
    db.add(novo_cliente)
    db.commit()
    db.refresh(novo_cliente)
    return novo_cliente


# Listar todos os clientes
@app.get("/clientes", response_model=list[schemas.ClienteResponse])
def listar_clientes(db: Session = Depends(get_db)):
    return db.query(models.Cliente).all()


# Buscar um cliente específico
@app.get("/clientes/{cliente_id}", response_model=schemas.ClienteResponse)
def buscar_cliente(cliente_id: int, db: Session = Depends(get_db)):
    cliente = db.query(models.Cliente).filter(models.Cliente.id == cliente_id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return cliente


# Deletar um cliente
@app.delete("/clientes/{cliente_id}")
def deletar_cliente(cliente_id: int, db: Session = Depends(get_db)):
    cliente = db.query(models.Cliente).filter(models.Cliente.id == cliente_id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    db.delete(cliente)
    db.commit()
    return {"mensagem": "Cliente deletado com sucesso"}

# Criar um pedido (com verificação de estoque)
@app.post("/pedidos", response_model=schemas.PedidoResponse)
def criar_pedido(pedido: schemas.PedidoCreate, db: Session = Depends(get_db)):
    # Verifica se o cliente existe
    cliente = db.query(models.Cliente).filter(models.Cliente.id == pedido.cliente_id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")

    # Primeiro, verifica se TODOS os produtos têm estoque suficiente
    for item in pedido.itens:
        produto = db.query(models.Produto).filter(models.Produto.id == item.produto_id).first()
        if not produto:
            raise HTTPException(status_code=404, detail=f"Produto {item.produto_id} não encontrado")
        if produto.quantidade_estoque < item.quantidade:
            raise HTTPException(
                status_code=400,
                detail=f"Estoque insuficiente para '{produto.nome}'. Disponível: {produto.quantidade_estoque}"
            )

    # Se passou pela verificação, cria o pedido
    novo_pedido = models.Pedido(cliente_id=pedido.cliente_id)
    db.add(novo_pedido)
    db.commit()
    db.refresh(novo_pedido)

    # Cria os itens do pedido e dá baixa no estoque
    for item in pedido.itens:
        produto = db.query(models.Produto).filter(models.Produto.id == item.produto_id).first()

        novo_item = models.ItemPedido(
            pedido_id=novo_pedido.id,
            produto_id=item.produto_id,
            quantidade=item.quantidade,
            preco_unitario=produto.preco
        )
        db.add(novo_item)

        produto.quantidade_estoque -= item.quantidade  # baixa no estoque

    db.commit()
    db.refresh(novo_pedido)
    return novo_pedido


# Listar todos os pedidos
@app.get("/pedidos", response_model=list[schemas.PedidoResponse])
def listar_pedidos(db: Session = Depends(get_db)):
    return db.query(models.Pedido).all()


# Buscar um pedido específico
@app.get("/pedidos/{pedido_id}", response_model=schemas.PedidoResponse)
def buscar_pedido(pedido_id: int, db: Session = Depends(get_db)):
    pedido = db.query(models.Pedido).filter(models.Pedido.id == pedido_id).first()
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    return pedido

# Registrar um novo usuário
@app.post("/registro", response_model=schemas.UsuarioResponse)
def registrar(usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    # Verifica se já existe usuário com esse email
    existente = db.query(models.Usuario).filter(models.Usuario.email == usuario.email).first()
    if existente:
        raise HTTPException(status_code=400, detail="Email já cadastrado")

    novo_usuario = models.Usuario(
        nome=usuario.nome,
        email=usuario.email,
        senha_hash=auth.hash_senha(usuario.senha)
    )
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)
    return novo_usuario


# Login - gera o token de acesso
@app.post("/login", response_model=schemas.TokenResponse)
def login(dados: schemas.LoginRequest, db: Session = Depends(get_db)):
    usuario = db.query(models.Usuario).filter(models.Usuario.email == dados.email).first()

    if not usuario or not auth.verificar_senha(dados.senha, usuario.senha_hash):
        raise HTTPException(status_code=401, detail="Email ou senha incorretos")

    token = auth.criar_token({"sub": usuario.email})
    return {"access_token": token, "token_type": "bearer"}

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=False)