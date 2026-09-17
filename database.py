import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Carrega as variáveis do arquivo .env
load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

# Monta a "URL" de conexão com o MySQL
DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Cria a conexão (engine) com o banco
engine = create_engine(DATABASE_URL)

# Cria as "sessões" - cada requisição da API vai usar uma sessão pra falar com o banco
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base que os "modelos" (tabelas em Python) vão herdar
Base = declarative_base()

# Função que a API vai usar para abrir e fechar conexões automaticamente
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()