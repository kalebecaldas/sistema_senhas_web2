import requests
from flask import current_app, Blueprint, send_file, request, make_response
import io

bp_tts = Blueprint('tts', __name__)

__all__ = ['bp_tts']

def gerar_audio_azure(texto, nome_voz='pt-BR-FranciscaNeural'):
    chave = "1GrRULjTQvppqKpUK2GSKc6YRwmdNdlDW4YywGXMfL6LkpfPU004JQQJ99BDACZoyfiXJ3w3AAAYACOGsj0S"
    endpoint = "https://brazilsouth.tts.speech.microsoft.com"
    url = f"{endpoint}/cognitiveservices/v1"

    headers = {
        "Ocp-Apim-Subscription-Key": chave,
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

    resposta = requests.post(url, headers=headers, data=ssml.encode('utf-8'))
    if resposta.status_code == 200:
        return resposta.content
    else:
        raise Exception(f"Erro Azure TTS: {resposta.status_code} - {resposta.text}")


@bp_tts.route('/tts_audio')
def tts_audio():
    from .models import ConfiguracaoSistema

    texto = request.args.get('texto', '')
    if not texto:
        return make_response("Texto não fornecido", 400)

    config = ConfiguracaoSistema.query.first()
    nome_voz = config.voz_azure if config and config.voz_azure else 'pt-BR-FranciscaNeural'

    try:
        audio_data = gerar_audio_azure(texto, nome_voz)
        return send_file(io.BytesIO(audio_data), mimetype='audio/mpeg', as_attachment=False, download_name='voz.mp3')
    except Exception as e:
        return make_response(str(e), 500)

