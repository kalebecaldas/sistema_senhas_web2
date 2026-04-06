#!/usr/bin/env python3
"""
Script de migração para adicionar colunas da playlist ao banco de dados
"""
import sqlite3
import os

# Caminho do banco de dados
DB_PATH = 'instance/sistema.db'

def migrate_database():
    """Adiciona as novas colunas ao banco de dados"""
    
    if not os.path.exists(DB_PATH):
        print(f"❌ Banco de dados não encontrado em: {DB_PATH}")
        return False
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Lista de colunas para adicionar
    columns_to_add = [
        ('playlist_enabled', 'INTEGER DEFAULT 0'),
        ('transition_type', 'VARCHAR(20) DEFAULT "fade"'),
        ('transition_duration', 'REAL DEFAULT 1.0'),
        ('play_order', 'VARCHAR(20) DEFAULT "sequential"'),
        ('tv_enabled', 'INTEGER DEFAULT 0'),
        ('tv_channel_id', 'VARCHAR(100)'),
        ('videos_before_tv', 'INTEGER DEFAULT 3'),
        ('tv_duration_minutes', 'INTEGER DEFAULT 10'),
    ]
    
    print("🔄 Iniciando migração do banco de dados...")
    
    for column_name, column_type in columns_to_add:
        try:
            # Verifica se a coluna já existe
            cursor.execute(f"PRAGMA table_info(configuracao_sistema)")
            columns = [col[1] for col in cursor.fetchall()]
            
            if column_name in columns:
                print(f"  ⏭️  Coluna '{column_name}' já existe, pulando...")
                continue
            
            # Adiciona a coluna
            sql = f"ALTER TABLE configuracao_sistema ADD COLUMN {column_name} {column_type}"
            cursor.execute(sql)
            print(f"  ✅ Coluna '{column_name}' adicionada com sucesso!")
            
        except sqlite3.Error as e:
            print(f"  ❌ Erro ao adicionar coluna '{column_name}': {e}")
            conn.rollback()
            return False
    
    # Cria a tabela video_playlist se não existir
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS video_playlist (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename VARCHAR(255) NOT NULL,
                path VARCHAR(255) NOT NULL,
                duration INTEGER,
                ordem INTEGER DEFAULT 0,
                ativo INTEGER DEFAULT 1,
                criado_em DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("  ✅ Tabela 'video_playlist' criada/verificada com sucesso!")
    except sqlite3.Error as e:
        print(f"  ❌ Erro ao criar tabela 'video_playlist': {e}")
        conn.rollback()
        return False
    
    # Commit das mudanças
    conn.commit()
    conn.close()
    
    print("\n✅ Migração concluída com sucesso!")
    print("🔄 Reinicie o servidor para aplicar as mudanças.")
    return True

if __name__ == '__main__':
    migrate_database()
