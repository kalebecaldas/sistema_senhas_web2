"""
Serviços centralizados para o sistema de senhas
"""
from datetime import datetime, timedelta
from random import choices
from typing import Optional, Tuple
from sqlalchemy.orm import Session

from .models import Senha, ConfiguracaoSistema


class PrioridadeService:
    """Serviço para gerenciar lógicas de prioridade de senhas"""
    
    def __init__(self, db_session: Session, config: ConfiguracaoSistema):
        self.db = db_session
        self.config = config
    
    def selecionar_senha_prioritaria(self) -> Optional[Senha]:
        """Seleciona a próxima senha preferencial"""
        return (self.db.query(Senha)
                .filter_by(chamado=False, tipo_paciente='preferencial')
                .order_by(Senha.id)
                .first())
    
    def selecionar_senha_normal(self) -> Optional[Senha]:
        """Seleciona a próxima senha normal"""
        return (self.db.query(Senha)
                .filter_by(chamado=False, tipo_paciente='normal')
                .order_by(Senha.id)
                .first())
    
    def contar_senhas_aguardando(self) -> Tuple[int, int]:
        """Conta senhas normais e preferenciais aguardando"""
        normais = self.db.query(Senha).filter_by(chamado=False, tipo_paciente='normal').count()
        preferenciais = self.db.query(Senha).filter_by(chamado=False, tipo_paciente='preferencial').count()
        return normais, preferenciais
    
    def aplicar_intercalamento(self, contador_normais: int) -> Tuple[Optional[Senha], int]:
        """Aplica lógica de intercalamento fixo"""
        valor = self.config.intercalamento_valor or 2
        
        if contador_normais >= valor:
            senha = self.selecionar_senha_prioritaria()
            novo_contador = 0
        else:
            senha = self.selecionar_senha_normal()
            novo_contador = contador_normais + 1
        
        # Fallback se não encontrar senha do tipo esperado
        if not senha:
            senha = self.selecionar_senha_prioritaria() or self.selecionar_senha_normal()
            novo_contador = 0
        
        return senha, novo_contador
    
    def aplicar_peso(self) -> Optional[Senha]:
        """Aplica lógica de sistema de peso"""
        normais, preferenciais = self.contar_senhas_aguardando()
        
        opcoes, pesos = [], []
        
        if normais > 0:
            opcoes.append('normal')
            pesos.append(self.config.peso_normal or 1)
        
        if preferenciais > 0:
            opcoes.append('preferencial')
            pesos.append(self.config.peso_preferencial or 3)
        
        if not opcoes:
            return None
        
        tipo_sorteado = choices(opcoes, weights=pesos, k=1)[0]
        
        if tipo_sorteado == 'normal':
            senha = self.selecionar_senha_normal()
            if not senha:
                senha = self.selecionar_senha_prioritaria()
        else:
            senha = self.selecionar_senha_prioritaria()
            if not senha:
                senha = self.selecionar_senha_normal()
        
        return senha
    
    def aplicar_alternancia(self) -> Optional[Senha]:
        """Aplica lógica de alternância dinâmica"""
        tolerancia = self.config.tolerancia_minutos or 5
        agora = datetime.utcnow()
        
        # Buscar senhas aguardando
        preferenciais = (self.db.query(Senha)
                        .filter_by(chamado=False, tipo_paciente='preferencial')
                        .order_by(Senha.id)
                        .all())
        
        normais = (self.db.query(Senha)
                  .filter_by(chamado=False, tipo_paciente='normal')
                  .order_by(Senha.id)
                  .all())
        
        # Verificar última senha preferencial chamada
        ultima_pref = (self.db.query(Senha)
                      .filter_by(chamado=True, tipo_paciente='preferencial')
                      .order_by(Senha.chamado_em.desc())
                      .first())
        
        # Calcular tempo de espera
        if ultima_pref and ultima_pref.chamado_em:
            tempo_espera = (agora - ultima_pref.chamado_em).total_seconds() / 60
        else:
            tempo_espera = tolerancia + 1
        
        # Log para debug
        print(f"[DEBUG Alternância] Espera atual: {tempo_espera:.2f} min | Tolerância: {tolerancia} min")
        
        # Decidir qual tipo chamar
        if tempo_espera > tolerancia:
            # Priorizar preferenciais se esperaram muito
            senha = preferenciais[0] if preferenciais else (normais[0] if normais else None)
        else:
            # Chamar normal se preferenciais não esperaram muito
            senha = normais[0] if normais else (preferenciais[0] if preferenciais else None)
        
        return senha
    
    def selecionar_proxima_senha(self, contador_normais: int = 0) -> Tuple[Optional[Senha], int]:
        """Seleciona a próxima senha baseada na configuração de prioridade"""
        tipo_prioridade = self.config.tipo_prioridade or 'intercalamento'
        
        if tipo_prioridade == 'intercalamento':
            senha, novo_contador = self.aplicar_intercalamento(contador_normais)
            return senha, novo_contador
        
        elif tipo_prioridade == 'peso':
            senha = self.aplicar_peso()
            return senha, contador_normais
        
        elif tipo_prioridade == 'alternancia':
            senha = self.aplicar_alternancia()
            return senha, contador_normais
        
        else:
            # Fallback para intercalamento
            return self.aplicar_intercalamento(contador_normais)


class ImpressoraService:
    """Serviço para gerenciar impressão de senhas"""
    
    def __init__(self):
        # Configurações de impressora - podem ser movidas para banco de dados
        self.impressoras = {
            'principal': {'ip': '192.168.0.245', 'porta': 9100},
            'secundaria': {'ip': '192.168.0.48', 'porta': 9100}
        }
    
    def gerar_comandos_escpos(self, senha_completa: str) -> bytes:
        """Gera comandos ESC/POS para impressão"""
        ESC = b'\x1b'
        GS = b'\x1d'
        
        comandos = b""
        comandos += ESC + b'@'  # Initialize printer
        comandos += ESC + b'a' + b'\x01'  # Center alignment
        comandos += b'\n'
        comandos += ESC + b'!' + b'\x38'  # Double height and width
        comandos += f"SENHA {senha_completa}\n".encode('utf-8')
        comandos += ESC + b'!' + b'\x00'  # Normal size
        comandos += ESC + b'a' + b'\x01'  # Center alignment
        comandos += b'\n\n'
        comandos += b"Aguarde ser chamado\n"
        comandos += b'\n\n\n\n\n\n'
        comandos += GS + b'V' + b'\x00'  # Cut paper
        
        return comandos
    
    def imprimir_senha(self, senha_completa: str, impressora: str = 'principal') -> bool:
        """Imprime uma senha na impressora especificada"""
        import socket
        
        try:
            config = self.impressoras.get(impressora, self.impressoras['principal'])
            comandos = self.gerar_comandos_escpos(senha_completa)
            
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)  # Timeout de 5 segundos
            sock.connect((config['ip'], config['porta']))
            sock.sendall(comandos)
            sock.close()
            
            return True
        except Exception as e:
            print(f'Erro ao imprimir senha: {e}')
            return False


class TTSService:
    """Serviço para síntese de voz"""
    
    def __init__(self, config: ConfiguracaoSistema):
        self.config = config
        self.chave_azure = "1GrRULjTQvppqKpUK2GSKc6YRwmdNdlDW4YywGXMfL6LkpfPU004JQQJ99BDACZoyfiXJ3w3AAAYACOGsj0S"
        self.endpoint_azure = "https://brazilsouth.tts.speech.microsoft.com"
    
    def gerar_audio(self, texto: str, nome_voz: str = '') -> bytes:
        """Gera áudio usando Azure TTS"""
        import requests
        
        if not nome_voz:
            nome_voz = self.config.voz_azure or 'pt-BR-FranciscaNeural'
        
        url = f"{self.endpoint_azure}/cognitiveservices/v1"
        
        headers = {
            "Ocp-Apim-Subscription-Key": self.chave_azure,
            "Content-Type": "application/ssml+xml",
            "X-Microsoft-OutputFormat": "audio-16khz-32kbitrate-mono-mp3",
            "User-Agent": "IAAM-SistemaSenhas"
        }
        
        ssml = f"""
        <speak version='1.0' xml:lang='pt-BR'>
          <voice xml:lang='pt-BR' name='{nome_voz}'>
            {texto}
          </voice>
        </speak>
        """
        
        resposta = requests.post(url, headers=headers, data=ssml.encode('utf-8'), timeout=10)
        
        if resposta.status_code == 200:
            return resposta.content
        else:
            raise Exception(f"Erro Azure TTS: {resposta.status_code} - {resposta.text}")
    
    def formatar_mensagem_voz(self, senha_completa: str, guiche: str) -> str:
        """Formata mensagem para síntese de voz"""
        # Verifica se é chamada personalizada (apenas texto)
        if senha_completa.isalpha():
            return f"{senha_completa}, dirija-se ao guichê {guiche}"
        
        # Formata senha numérica - versão Python
        import re
        match = re.match(r'(\D+)(\d+)', senha_completa)
        if match:
            prefixo, numero = match.groups()
            spelled = ' '.join(prefixo + numero)
        else:
            spelled = ' '.join(senha_completa)
        
        return f"Senha {spelled}, dirija-se ao guichê {guiche}" 