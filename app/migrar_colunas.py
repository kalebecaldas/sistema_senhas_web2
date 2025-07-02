from app import db
from sqlalchemy import text

# Executa o comando direto no banco
with db.engine.connect() as conn:
    conn.execute(text("ALTER TABLE senha ADD COLUMN guiche VARCHAR(10);"))
    conn.commit()
