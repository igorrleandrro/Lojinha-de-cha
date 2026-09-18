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