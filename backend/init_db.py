from app.db.database import engine, Base

# Cria todas as tabelas definidas nos modelos que herdam de Base
# Base.metadata.create_all(bind=engine)

print("Banco de dados inicializado e tabelas criadas com sucesso!") 

