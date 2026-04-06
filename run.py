from app import create_app

app = create_app()

if __name__ == "__main__":
    # Configuração otimizada para produção com suporte a múltiplas requisições simultâneas
    app.run(
        host="0.0.0.0", 
        port=5003, 
        debug=False,  # Desabilitar debug para melhor performance
        threaded=True,  # Habilitar threads para requisições simultâneas
        use_reloader=False  # Desabilitar reloader para evitar travamentos
    )
