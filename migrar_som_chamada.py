"""
Migração: adiciona coluna som_chamada à tabela configuracao_sistema.
Execute uma única vez: python migrar_som_chamada.py
"""
from app import create_app, db
from sqlalchemy import text, inspect

app = create_app()

with app.app_context():
    inspector = inspect(db.engine)
    cols = [c['name'] for c in inspector.get_columns('configuracao_sistema')]
    if 'som_chamada' not in cols:
        with db.engine.connect() as conn:
            conn.execute(text(
                "ALTER TABLE configuracao_sistema "
                "ADD COLUMN som_chamada VARCHAR(30) DEFAULT 'sino_suave';"
            ))
            conn.commit()
        print("Coluna som_chamada adicionada com sucesso.")
    else:
        print("Coluna som_chamada já existe, nada a fazer.")
