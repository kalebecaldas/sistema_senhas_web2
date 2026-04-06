"""
Serviços centralizados para o sistema de senhas
"""
import os
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
        
        # Debug para verificar o comportamento
        print(f"[DEBUG Intercalamento] Contador atual: {contador_normais}, Valor esperado: {valor}")
        
        # Verificar se atingiu o número de normais necessárias
        if contador_normais >= valor:
            # Chamar preferencial e resetar contador
            senha = self.selecionar_senha_prioritaria()
            novo_contador = 0
            print(f"[DEBUG] Chamando PREFERENCIAL após {contador_normais} normais")
        else:
            # Chamar normal e incrementar contador
            senha = self.selecionar_senha_normal()
            novo_contador = contador_normais + 1
            print(f"[DEBUG] Chamando NORMAL #{novo_contador}/{valor}")
        
        # Fallback se não encontrar senha do tipo esperado
        if not senha:
            print(f"[DEBUG] Fallback necessário - buscando qualquer senha disponível")
            senha = self.selecionar_senha_prioritaria() or self.selecionar_senha_normal()
            novo_contador = 0
        
        return senha, novo_contador
    
    def aplicar_peso(self) -> Optional[Senha]:
        """Aplica lógica de sistema de peso"""
        normais, preferenciais = self.contar_senhas_aguardando()
        
        print(f"[DEBUG Peso] Esperando: {normais} normais, {preferenciais} preferenciais")
        
        opcoes, pesos = [], []
        
        if normais > 0:
            peso_n = self.config.peso_normal or 1
            opcoes.append('normal')
            pesos.append(peso_n)
            print(f"[DEBUG] Peso normal: {peso_n}")
        
        if preferenciais > 0:
            peso_p = self.config.peso_preferencial or 3
            opcoes.append('preferencial')
            pesos.append(peso_p)
            print(f"[DEBUG] Peso preferencial: {peso_p}")
        
        if not opcoes:
            print("[DEBUG] Nenhuma senha disponível")
            return None
        
        print(f"[DEBUG] Opções disponíveis: {opcoes}, Pesos: {pesos}")
        tipo_sorteado = choices(opcoes, weights=pesos, k=1)[0]
        print(f"[DEBUG] Tipo sorteado: {tipo_sorteado}")
        
        if tipo_sorteado == 'normal':
            senha = self.selecionar_senha_normal()
            if not senha:
                print("[DEBUG] Fallback: NORMAL não encontrada, buscando PREFERENCIAL")
                senha = self.selecionar_senha_prioritaria()
        else:
            senha = self.selecionar_senha_prioritaria()
            if not senha:
                print("[DEBUG] Fallback: PREFERENCIAL não encontrada, buscando NORMAL")
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
        
        print(f"[DEBUG Alternância] Aguardando: {len(normais)} normais, {len(preferenciais)} preferenciais")
        
        # Verificar última senha preferencial chamada
        ultima_pref = (self.db.query(Senha)
                      .filter_by(chamado=True, tipo_paciente='preferencial')
                      .order_by(Senha.chamado_em.desc())
                      .first())
        
        # Calcular tempo de espera desde a última preferencial
        if ultima_pref and ultima_pref.chamado_em:
            tempo_espera = (agora - ultima_pref.chamado_em).total_seconds() / 60
            print(f"[DEBUG] Última preferencial chamada há: {tempo_espera:.2f} min")
        else:
            tempo_espera = 0  # Se nunca houve preferencial chamada
            print("[DEBUG] Nenhuma preferencial foi chamada ainda")
        
        # Decidir qual tipo chamar baseado no tempo de espera
        if tempo_espera >= tolerancia:
            # Se preferenciais esperaram muito (> tolerância), priorizar eles
            senha = preferenciais[0] if preferenciais else (normais[0] if normais else None)
            print(f"[DEBUG] TOLERÂNCIA ATINGIDA ({tempo_espera:.1f} >= {tolerancia}min) - Chamando PREFERENCIAL")
        else:
            # Se ainda não atingiu tolerância, pode chamar normal
            senha = normais[0] if normais else (preferenciais[0] if preferenciais else None)
            tipo_chamado = 'NORMAL' if normais else 'PREFERENCIAL'
            print(f"[DEBUG] Dentro da tolerância ({tempo_espera:.1f}/{tolerancia}min) - Chamando {tipo_chamado}")
        
        return senha
    
    def selecionar_proxima_senha(self, contador_normais: int = 0) -> Tuple[Optional[Senha], int]:
        """Seleciona a próxima senha baseada na configuração de prioridade"""
        tipo_prioridade = self.config.tipo_prioridade or 'intercalamento'
        
        print(f"[DEBUG PRIORIDADE] === Iniciando seleção de senha ===")
        print(f"[DEBUG PRIORIDADE] Tipo configurado: {tipo_prioridade}")
        print(f"[DEBUG PRIORIDADE] Contador normais atual: {contador_normais}")
        
        if tipo_prioridade == 'intercalamento':
            print("[DEBUG PRIORIDADE] Aplicando LÓGICA: Intercalamento Fixo")
            senha, novo_contador = self.aplicar_intercalamento(contador_normais)
        
        elif tipo_prioridade == 'peso':
            print("[DEBUG PRIORIDADE] Aplicando LÓGICA: Sistema de Peso")
            senha = self.aplicar_peso()
            novo_contador = contador_normais
        
        elif tipo_prioridade == 'alternancia':
            print("[DEBUG PRIORIDADE] Aplicando LÓGICA: Alternância Dinâmica")
            senha = self.aplicar_alternancia()
            novo_contador = contador_normais
        
        else:
            print("[DEBUG PRIORIDADE] Tipo desconhecido, usando FALLBACK: Intercalamento")
            senha, novo_contador = self.aplicar_intercalamento(contador_normais)
        
        if senha:
            print(f"[DEBUG PRIORIDADE] ✅ Senha selecionada: {senha.sigla}{senha.numero:04d} ({senha.tipo_paciente})")
        else:
            print(f"[DEBUG PRIORIDADE] ❌ SENHA NULO - Nenhuma senha encontrada")
        
        print(f"[DEBUG PRIORIDADE] === Fim da seleção ===")
        return senha, novo_contador


class ImpressoraService:
    """Serviço para gerenciar impressão de senhas"""
    
    def __init__(self, config: ConfiguracaoSistema = None):
        # Buscar configurações do banco de dados ou usar padrões
        if config:
            self.impressoras = {
                'principal': {
                    'ip': config.impressora_principal_ip or '192.168.0.245',
                    'porta': config.impressora_principal_porta or 9100
                },
                'secundaria': {
                    'ip': config.impressora_secundaria_ip or '192.168.0.48',
                    'porta': config.impressora_secundaria_porta or 9100
                }
            }
        else:
            # Fallback caso não tenha config
            self.impressoras = {
                'principal': {'ip': '192.168.0.245', 'porta': 9100},
                'secundaria': {'ip': '192.168.0.48', 'porta': 9100}
            }
    
    def gerar_comandos_escpos(self, senha_completa: str) -> bytes:
        """Gera comandos ESC/POS para impressão com formatação melhorada"""
        from datetime import datetime
        from zoneinfo import ZoneInfo
        
        ESC = b'\x1b'
        GS = b'\x1d'
        
        # Obter data e hora atual no fuso horário de Manaus
        TZ_MANAUS = ZoneInfo('America/Manaus')
        agora = datetime.now(TZ_MANAUS)
        data_hora = agora.strftime('%d/%m/%Y - %H:%M:%S')
        
        # Determinar tipo de senha
        tipo_senha = "NORMAL"
        if senha_completa.startswith('PP') or senha_completa.startswith('PR'):
            tipo_senha = "PREFERENCIAL"
        
        comandos = b""
        
        # Inicializar impressora
        comandos += ESC + b'@'
        comandos += b'\n'
        
        # Cabeçalho - Nome da instituição
        comandos += ESC + b'a' + b'\x01'  # Centralizar
        comandos += ESC + b'!' + b'\x10'  # Fonte grande
        comandos += b"================================\n"
        comandos += ESC + b'!' + b'\x20'  # Fonte dupla altura
        comandos += b"IAAM\n"
        comandos += ESC + b'!' + b'\x00'  # Fonte normal
        comandos += b"Sistema de Senhas\n"
        comandos += b"================================\n"
        comandos += b'\n'
        
        # Tipo de atendimento
        comandos += ESC + b'!' + b'\x10'  # Fonte média
        comandos += f"Tipo: {tipo_senha}\n".encode('utf-8')
        comandos += ESC + b'!' + b'\x00'  # Fonte normal
        comandos += b'\n'
        
        # Número da senha - DESTAQUE
        comandos += b"--------------------------------\n"
        comandos += ESC + b'!' + b'\x38'  # Dupla altura e largura
        comandos += b"  SENHA  \n"
        comandos += b'\n'
        comandos += f" {senha_completa} \n".encode('utf-8')
        comandos += b'\n'
        comandos += ESC + b'!' + b'\x00'  # Fonte normal
        comandos += b"--------------------------------\n"
        comandos += b'\n\n'
        
        # Data e hora
        comandos += ESC + b'!' + b'\x00'  # Fonte normal
        comandos += f"{data_hora}\n".encode('utf-8')
        comandos += b'\n\n'
        
        # Instruções
        comandos += b"--------------------------------\n"
        comandos += ESC + b'!' + b'\x10'  # Fonte média
        comandos += b"   AGUARDE SER CHAMADO   \n"
        comandos += ESC + b'!' + b'\x00'  # Fonte normal
        comandos += b"--------------------------------\n"
        comandos += b'\n'
        comandos += b"Fique atento ao painel\n"
        comandos += b"de chamadas\n"
        comandos += b'\n'
        comandos += b"Obrigado pela preferencia!\n"
        comandos += b'\n\n\n\n\n\n'
        
        # Cortar papel
        comandos += GS + b'V' + b'\x00'
        
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
        self.chave_azure = (os.environ.get('TTS_AZURE_KEY') or '').strip()
        self.endpoint_azure = (
            os.environ.get('TTS_AZURE_ENDPOINT') or 'https://brazilsouth.tts.speech.microsoft.com'
        ).rstrip('/')

    def gerar_audio(self, texto: str, nome_voz: str = '') -> bytes:
        """Gera áudio usando Azure TTS"""
        import requests

        if not self.chave_azure:
            raise RuntimeError('TTS Azure não configurado: defina a variável TTS_AZURE_KEY.')
        
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