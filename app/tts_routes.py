from flask import Blueprint, send_file, request, make_response
import io

from .models import ConfiguracaoSistema
from .services import TTSService

bp_tts = Blueprint('tts', __name__)

__all__ = ['bp_tts']


@bp_tts.route('/tts_audio')
def tts_audio():
    texto = request.args.get('texto', '')
    if not texto:
        return make_response("Texto não fornecido", 400)

    config = ConfiguracaoSistema.query.first()
    if not config:
        return make_response("Configuração não encontrada", 500)

    try:
        tts_service = TTSService(config)
        audio_data = tts_service.gerar_audio(texto)
        return send_file(io.BytesIO(audio_data), mimetype='audio/mpeg', as_attachment=False, download_name='voz.mp3')
    except Exception as e:
        return make_response(str(e), 500)

