from app import create_app, db
from sqlalchemy import text

# Cria a instância do app e aplica o contexto
app = create_app()

def adicionar_coluna_guiche():
    with app.app_context():
        try:
            with db.engine.connect() as conn:
                conn.execute(text("ALTER TABLE senha ADD COLUMN guiche VARCHAR(10);"))
                conn.commit()
                print("✅ Coluna 'guiche' adicionada com sucesso.")
        except Exception as e:
            if "duplicate column" in str(e).lower() or "already exists" in str(e).lower():
                print("⚠️ A coluna 'guiche' já existe.")
            else:
                print("❌ Erro ao adicionar a coluna:", e)

if __name__ == "__main__":
    adicionar_coluna_guiche()
