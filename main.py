from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db, engine, Base
import models
import schemas

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