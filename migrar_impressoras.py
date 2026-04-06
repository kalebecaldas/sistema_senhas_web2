"""
Script de migração para adicionar colunas de configuração de impressoras
"""
from app import create_app, db
from app.models import ConfiguracaoSistema

app = create_app()

with app.app_context():
    try:
        # Adicionar colunas se não existirem
        from sqlalchemy import text
        
        with db.engine.connect() as conn:
            # Verificar se as colunas já existem
            result = conn.execute(text("PRAGMA table_info(configuracao_sistema)"))
            colunas_existentes = [row[1] for row in result]
            
            print(f"Colunas existentes: {colunas_existentes}")
            
            # Adicionar colunas se não existirem
            if 'impressora_principal_ip' not in colunas_existentes:
                print("Adicionando coluna: impressora_principal_ip")
                conn.execute(text(
                    "ALTER TABLE configuracao_sistema ADD COLUMN impressora_principal_ip VARCHAR(15) DEFAULT '192.168.0.245'"
                ))
                conn.commit()
            
            if 'impressora_principal_porta' not in colunas_existentes:
                print("Adicionando coluna: impressora_principal_porta")
                conn.execute(text(
                    "ALTER TABLE configuracao_sistema ADD COLUMN impressora_principal_porta INTEGER DEFAULT 9100"
                ))
                conn.commit()
            
            if 'impressora_secundaria_ip' not in colunas_existentes:
                print("Adicionando coluna: impressora_secundaria_ip")
                conn.execute(text(
                    "ALTER TABLE configuracao_sistema ADD COLUMN impressora_secundaria_ip VARCHAR(15) DEFAULT '192.168.0.48'"
                ))
                conn.commit()
            
            if 'impressora_secundaria_porta' not in colunas_existentes:
                print("Adicionando coluna: impressora_secundaria_porta")
                conn.execute(text(
                    "ALTER TABLE configuracao_sistema ADD COLUMN impressora_secundaria_porta INTEGER DEFAULT 9100"
                ))
                conn.commit()
        
        print("OK - Migracao concluida com sucesso!")
        print("Agora voce pode configurar os IPs das impressoras em 'Editar Telas' -> Aba 'Textos'")
        
    except Exception as e:
        print(f"ERRO - Erro na migracao: {e}")
        import traceback
        traceback.print_exc()
