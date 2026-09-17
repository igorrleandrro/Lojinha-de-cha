from database import SessionLocal
from models import Categoria

# Abre uma sessão com o banco
db = SessionLocal()

# Tenta buscar todas as categorias (a tabela existe, mas está vazia ainda)
categorias = db.query(Categoria).all()

print(f"Conexão funcionando! Encontradas {len(categorias)} categorias no banco.")

db.close()