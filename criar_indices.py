"""
Script para criar índices no banco de dados para melhorar a performance
Execute este script uma vez após atualizar o sistema
"""
from app import create_app, db
from sqlalchemy import text

app = create_app()

with app.app_context():
    print("🔧 Criando índices no banco de dados...")
    
    try:
        # Criar índices se não existirem
        with db.engine.connect() as conn:
            # Índice para chamado
            try:
                conn.execute(text("CREATE INDEX IF NOT EXISTS idx_senha_chamado ON senha(chamado);"))
                print("✅ Índice idx_senha_chamado criado")
            except Exception as e:
                print(f"⚠️ Índice idx_senha_chamado já existe ou erro: {e}")
            
            # Índice para chamado_em
            try:
                conn.execute(text("CREATE INDEX IF NOT EXISTS idx_senha_chamado_em ON senha(chamado_em);"))
                print("✅ Índice idx_senha_chamado_em criado")
            except Exception as e:
                print(f"⚠️ Índice idx_senha_chamado_em já existe ou erro: {e}")
            
            # Índice para gerado_em
            try:
                conn.execute(text("CREATE INDEX IF NOT EXISTS idx_senha_gerado_em ON senha(gerado_em);"))
                print("✅ Índice idx_senha_gerado_em criado")
            except Exception as e:
                print(f"⚠️ Índice idx_senha_gerado_em já existe ou erro: {e}")
            
            # Índice composto para chamado + chamado_em (mais importante)
            try:
                conn.execute(text("CREATE INDEX IF NOT EXISTS idx_chamado_chamado_em ON senha(chamado, chamado_em);"))
                print("✅ Índice idx_chamado_chamado_em criado")
            except Exception as e:
                print(f"⚠️ Índice idx_chamado_chamado_em já existe ou erro: {e}")
            
            # Índice composto para tipo_paciente + chamado
            try:
                conn.execute(text("CREATE INDEX IF NOT EXISTS idx_tipo_chamado ON senha(tipo_paciente, chamado);"))
                print("✅ Índice idx_tipo_chamado criado")
            except Exception as e:
                print(f"⚠️ Índice idx_tipo_chamado já existe ou erro: {e}")
            
            conn.commit()
        
        print("\n✅ Índices criados com sucesso!")
        print("🚀 As queries agora serão muito mais rápidas!")
        
    except Exception as e:
        print(f"❌ Erro ao criar índices: {e}")
        import traceback
        traceback.print_exc()
