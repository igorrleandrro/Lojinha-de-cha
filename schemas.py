from pydantic import BaseModel


# Formato dos dados que a API RECEBE para criar uma categoria
class CategoriaCreate(BaseModel):
    nome: str


# Formato dos dados que a API DEVOLVE (inclui o id, que o banco gera sozinho)
class CategoriaResponse(BaseModel):
    id: int
    nome: str

    class Config:
        from_attributes = True


from typing import Optional


class ProdutoCreate(BaseModel):
    nome: str
    descricao: Optional[str] = None
    preco: float
    quantidade_estoque: int = 0
    categoria_id: int


class ProdutoResponse(BaseModel):
    id: int
    nome: str
    descricao: Optional[str] = None
    preco: float
    quantidade_estoque: int
    categoria_id: int

    class Config:
        from_attributes = True

class ClienteCreate(BaseModel):
    nome: str
    email: Optional[str] = None
    telefone: Optional[str] = None


class ClienteResponse(BaseModel):
    id: int
    nome: str
    email: Optional[str] = None
    telefone: Optional[str] = None

    class Config:
        from_attributes = True


from datetime import datetime


class ItemPedidoCreate(BaseModel):
    produto_id: int
    quantidade: int


class ItemPedidoResponse(BaseModel):
    id: int
    produto_id: int
    quantidade: int
    preco_unitario: float

    class Config:
        from_attributes = True


class PedidoCreate(BaseModel):
    cliente_id: int
    itens: list[ItemPedidoCreate]


class PedidoResponse(BaseModel):
    id: int
    cliente_id: int
    data_pedido: datetime
    status: str
    itens: list[ItemPedidoResponse]

    class Config:
        from_attributes = True