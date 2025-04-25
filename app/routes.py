from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify, session
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import os
from werkzeug.utils import secure_filename

from .models import Usuario, Senha, ConfiguracaoSistema
from . import db
from .auth_utils import role_required

import requests
from flask import send_file
from io import BytesIO
from .tts_routes import gerar_audio_azure


bp = Blueprint("main", __name__)

from datetime import datetime, timedelta
from flask import g

@bp.before_request
def controlar_sessao_por_inatividade():
    # Rotas que não devem ser afetadas pela inatividade
    rotas_livres = ['main.retira_senha', 'main.display']
    if request.endpoint in rotas_livres:
        return

    if current_user.is_authenticated:
        session.permanent = True
        bp.permanent_session_lifetime = timedelta(minutes=15)

        agora = datetime.utcnow()
        ultimo_uso = session.get('ultimo_uso')

        if ultimo_uso:
            try:
                delta = agora - datetime.fromisoformat(ultimo_uso)
                if delta.total_seconds() > 60 * 15:
                    logout_user()
                    session.clear()
                    flash("Sessão encerrada por inatividade.")
                    return redirect(url_for('main.login'))
            except ValueError:
                session['ultimo_uso'] = agora.isoformat()
        else:
            session['ultimo_uso'] = agora.isoformat()

        session['ultimo_uso'] = agora.isoformat()



# ---------- Rotas públicas ----------

@bp.route('/')
def home():
    return redirect(url_for('main.login'))

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.painel'))

    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        user = Usuario.query.filter_by(email=email).first()
        if user and check_password_hash(user.senha, senha):
            login_user(user)
            session.pop('guiche', None)
            return redirect(url_for('main.painel'))
        flash('Login ou senha inválidos')
    config = ConfiguracaoSistema.query.first()
    return render_template('login.html', config=config)

@bp.route('/retira')
def retira_senha():
    config = ConfiguracaoSistema.query.first()
    return render_template('gerar_senha.html', config=config, exibir_menu=False)

import socket

@bp.route('/api/retirar')
def api_retira_senha():
    ultima = Senha.query.order_by(Senha.id.desc()).first()
    numero = (ultima.numero + 1) if ultima else 1

    nova = Senha(numero=numero)
    db.session.add(nova)
    db.session.commit()

    ESC = b'\x1b'
    GS  = b'\x1d'

    comandos = b""
    comandos += ESC + b'@'
    comandos += ESC + b'a' + b'\x01'
    comandos += b'\n'
    comandos += ESC + b'!' + b'\x38'
    comandos += f"SENHA\n{numero}\n".encode('utf-8')
    comandos += ESC + b'!' + b'\x00'
    comandos += ESC + b'a' + b'\x01'
    comandos += b'\n\n'
    comandos += b"Aguarde ser chamado\n"
    comandos += b'\n\n\n\n\n\n'
    comandos += GS + b'V' + b'\x00'

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(('192.168.1.65', 9100))
        sock.sendall(comandos)
        sock.close()
    except Exception as e:
        print('Erro ao imprimir:', e)

    return jsonify({'numero': numero})

@bp.route('/api/gerar_senha')
def gerar_senha_triada():
    tipo = request.args.get('tipo')
    primeira = request.args.get('primeira') == 'true'

    if tipo == 'normal' and primeira:
        sigla = 'NP'
    elif tipo == 'normal' and not primeira:
        sigla = 'NR'
    elif tipo == 'preferencial' and primeira:
        sigla = 'PP'
    elif tipo == 'preferencial' and not primeira:
        sigla = 'PR'
    else:
        return jsonify({'erro': 'Parâmetros inválidos'}), 400

    from datetime import datetime, time
    agora = datetime.now()
    inicio_dia = datetime.combine(agora.date(), time.min)

    count = Senha.query.filter(Senha.gerado_em >= inicio_dia).count()

    numero = count + 1
    numero_formatado = str(numero).zfill(4)

    nova = Senha(
        sigla=sigla,
        numero=numero,
        chamado=False,
        gerado_em=agora,
        tipo_paciente=tipo,
        primeira_vez=primeira
    )
    db.session.add(nova)
    db.session.commit()

    senha_completa = f"{sigla}{numero_formatado}"

    return jsonify({
        'sigla': sigla,
        'numero': numero,
        'completo': senha_completa
    })

@bp.route('/display')
def display():
    senhas = Senha.query.filter_by(chamado=True).order_by(Senha.id.desc()).limit(15).all()
    config = ConfiguracaoSistema.query.first()
    return render_template('display.html', senhas=senhas, config=config, exibir_menu=False)

@bp.route('/fila_json')
def fila_json():
    dados = [
        {
            'id': s.id,  # Adicionado para controle de chamada
            'sigla': s.sigla,
            'numero': s.numero,
            'chamado': s.chamado,
            'chamado_em': s.chamado_em.isoformat() if s.chamado_em else None,
            'senha_completa': s.sigla if s.numero == 0 else f"{s.sigla}{str(s.numero).zfill(4)}"
        }
        for s in Senha.query.filter_by(chamado=True).order_by(Senha.id.desc()).all()
    ]
    return jsonify(dados)



# ---------- Rotas protegidas ----------

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    session.pop('guiche', None)
    return redirect(url_for('main.login'))

@bp.route('/painel')
@login_required
@role_required('admin', 'usuario')
def painel():
    from datetime import datetime

    # Lê o guichê salvo (pode vir vazio)
    guiche = session.get('guiche', '')

    # Busca última chamada do usuário
    ultima_chamada = Senha.query.filter_by(chamado_por=current_user.id) \
        .order_by(Senha.chamado_em.desc()).first()

    # Prepara a fila (limitada a 15)
    fila = Senha.query.order_by(
        Senha.chamado.asc(),
        Senha.chamado_em.desc().nullslast(),
        Senha.id.asc()
    ).limit(15).all()

    config = ConfiguracaoSistema.query.first()

    return render_template(
        'painel.html',
        usuario=current_user,
        fila=fila,
        config=config,
        guiche=guiche,
        ultima_chamada=ultima_chamada
    )






@bp.route('/chamar_senha')
@login_required
@role_required('admin', 'usuario')
def chamar_senha():
    from datetime import datetime
    from random import choices

    config = ConfiguracaoSistema.query.first()
    guiche = request.args.get("guiche") or session.get("guiche") or ""
    session['guiche'] = guiche

    if not guiche:
        flash("Informe o número do guichê antes de realizar chamadas.")
        return redirect(url_for('main.painel'))

    def selecionar_senha_prioritaria():
        return Senha.query.filter_by(chamado=False, tipo_paciente='preferencial').order_by(Senha.id).first()

    def selecionar_senha_normal():
        return Senha.query.filter_by(chamado=False, tipo_paciente='normal').order_by(Senha.id).first()

    senha = None

    if config.tipo_prioridade == 'intercalamento':
        contador = session.get('contador_normais', 0)
        valor = config.intercalamento_valor or 2

        if contador >= valor:
            senha = selecionar_senha_prioritaria()
            if senha:
                session['contador_normais'] = 0
        if not senha:
            senha = selecionar_senha_normal()
            session['contador_normais'] = session.get('contador_normais', 0) + 1

    elif config.tipo_prioridade == 'peso':
        peso_n = config.peso_normal or 1
        peso_p = config.peso_preferencial or 3
        opcoes, pesos = [], []

        if Senha.query.filter_by(chamado=False, tipo_paciente='normal').count():
            opcoes.append('normal')
            pesos.append(peso_n)
        if Senha.query.filter_by(chamado=False, tipo_paciente='preferencial').count():
            opcoes.append('preferencial')
            pesos.append(peso_p)

        if opcoes:
            tipo_sorteado = choices(opcoes, weights=pesos, k=1)[0]
            senha = selecionar_senha_normal() if tipo_sorteado == 'normal' else selecionar_senha_prioritaria()
            if not senha:
                senha = selecionar_senha_prioritaria() if tipo_sorteado == 'normal' else selecionar_senha_normal()

    elif config.tipo_prioridade == 'alternancia':
        tolerancia = config.tolerancia_minutos or 5
        agora = datetime.now()
        preferenciais = Senha.query.filter_by(chamado=False, tipo_paciente='preferencial').order_by(Senha.id).all()
        normais = Senha.query.filter_by(chamado=False, tipo_paciente='normal').order_by(Senha.id).all()

        ultima_pref = Senha.query.filter_by(chamado=True, tipo_paciente='preferencial')\
            .order_by(Senha.chamado_em.desc()).first()

        tempo_espera = (
            (agora - ultima_pref.chamado_em).total_seconds() / 60
            if ultima_pref and ultima_pref.chamado_em else tolerancia + 1
        )

        if tempo_espera > tolerancia:
            senha = preferenciais[0] if preferenciais else (normais[0] if normais else None)
        else:
            senha = normais[0] if normais else (preferenciais[0] if preferenciais else None)

    if senha:
        senha.chamado = True
        senha.chamado_por = current_user.id
        senha.chamado_em = datetime.utcnow()  # ✅ GARANTIR QUE É ATUALIZADO
        senha.guiche = guiche
        db.session.commit()

        session['mensagem_voz'] = f"Senha {senha.sigla}{str(senha.numero).zfill(4)}, dirija-se ao guichê {guiche}"
        flash(session['mensagem_voz'])
    else:
        flash("Nenhuma senha na fila.")

    return redirect(url_for('main.painel'))



@bp.route('/usuarios')
@login_required
@role_required('admin')
def listar_usuarios():
    usuarios = Usuario.query.order_by(Usuario.id).all()
    config = ConfiguracaoSistema.query.first()
    return render_template('usuarios.html', usuarios=usuarios, config=config)

@bp.route('/usuarios/<int:id>/editar', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def editar_usuario(id):
    usuario = Usuario.query.get_or_404(id)

    if request.method == 'POST':
        usuario.nome = request.form['nome']
        usuario.email = request.form['email']
        usuario.tipo = request.form['tipo']

        nova_senha = request.form['senha']
        if nova_senha:
            usuario.senha = generate_password_hash(nova_senha)

        db.session.commit()
        flash('Usuário atualizado com sucesso.')
        return redirect(url_for('main.listar_usuarios'))

    config = ConfiguracaoSistema.query.first()
    return render_template('editar_usuario.html', usuario=usuario, config=config)

@bp.route('/cadastro', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        tipo = request.form['tipo']

        if Usuario.query.filter_by(email=email).first():
            flash('Este e-mail já está cadastrado.')
            return redirect(url_for('main.cadastro'))

        novo = Usuario(
            nome=nome,
            email=email,
            senha=generate_password_hash(senha),
            tipo=tipo
        )
        db.session.add(novo)
        db.session.commit()
        flash('Usuário cadastrado com sucesso!')
        return redirect(url_for('main.painel'))

    config = ConfiguracaoSistema.query.first()
    return render_template('cadastro.html', config=config)

@bp.route('/edtelas')
@login_required
@role_required('admin')
def edtelas():
    print("➡️ Rota /edtelas carregada")
    config = ConfiguracaoSistema.query.first()
    return render_template('EdTelas.html', config=config)

@bp.route('/salvar_config', methods=['POST'])
@login_required
@role_required('admin')
def salvar_config():
    config = ConfiguracaoSistema.query.first()
    if not config:
        config = ConfiguracaoSistema()
        db.session.add(config)

    if 'reset_cores' in request.form:
        config.cor_fundo = "#000000"
        config.cor_texto = "#FFFFFF"
        config.cor_rodape = "#000000"
        config.contorno_senha = "#000000"
        config.linha_senha = "red"
        config.fundo_senha = "rgba(255, 255, 255, 0.03)"
        config.destaque_senha = "red"
        config.cor_bemvindo = "white"
        config.frase_bemvindo = "BEM-VINDO AO IAAM"
        config.cor_hora = "white"
    else:
        config.cor_fundo = request.form.get('cor_fundo', config.cor_fundo)
        config.cor_texto = request.form.get('cor_texto', config.cor_texto)
        config.cor_rodape = request.form.get('cor_rodape', config.cor_rodape)
        config.contorno_senha = request.form.get('contorno_senha', config.contorno_senha)
        config.linha_senha = request.form.get('linha_senha', config.linha_senha)
        config.fundo_senha = request.form.get('fundo_senha', config.fundo_senha)
        config.destaque_senha = request.form.get('destaque_senha', config.destaque_senha)
        config.cor_bemvindo = request.form.get('cor_bemvindo', config.cor_bemvindo)
        config.frase_bemvindo = request.form.get('frase_bemvindo', config.frase_bemvindo)
        config.cor_hora = request.form.get('cor_hora', config.cor_hora)
        config.voz_azure = request.form.get('voz_azure', config.voz_azure)

        # 🧠 NOVO BLOCO: prioridade de senhas
        config.tipo_prioridade = request.form.get('tipo_prioridade', config.tipo_prioridade)

        if config.tipo_prioridade == 'intercalamento':
            try:
                valor = int(request.form.get('intercalamento_valor', 2))
                if valor not in [2, 3]:
                    flash("Valor de intercalamento inválido. Somente 2 ou 3 são permitidos.")
                else:
                    config.intercalamento_valor = valor
            except ValueError:
                flash("O valor de intercalamento deve ser um número inteiro.")
        
        elif config.tipo_prioridade == 'peso':
            try:
                peso_n = int(request.form.get('peso_normal', 1))
                peso_p = int(request.form.get('peso_preferencial', 3))
                if peso_n < 1 or peso_p < 1:
                    flash("Os pesos devem ser inteiros maiores que zero.")
                else:
                    config.peso_normal = peso_n
                    config.peso_preferencial = peso_p
            except ValueError:
                flash("Os valores de peso devem ser numéricos inteiros.")

        elif config.tipo_prioridade == 'alternancia':
            try:
                minutos = int(request.form.get('tolerancia_minutos', 5))
                if minutos < 1 or minutos > 60:
                    flash("A tolerância deve estar entre 1 e 60 minutos.")
                else:
                    config.tolerancia_minutos = minutos
            except ValueError:
                flash("Tolerância deve ser um número inteiro.")

    if 'logo' in request.files:
        logo = request.files['logo']
        if logo.filename:
            logo_filename = secure_filename(logo.filename)
            logo.save(os.path.join('app/static/img', logo_filename))
            config.logo_path = f"img/{logo_filename}"

    if 'video' in request.files:
        video = request.files['video']
        if video.filename:
            video_filename = secure_filename(video.filename)
            video.save(os.path.join('app/static/videos', video_filename))
            config.video_path = f"videos/{video_filename}"

    db.session.commit()
    flash("Configurações salvas com sucesso!")
    return redirect(url_for('main.edtelas'))



@bp.route('/ultima_chamada')
def ultima_chamada():
    senha = Senha.query.filter_by(chamado=True).order_by(Senha.chamado_em.desc()).first()
    if senha:
        senha_completa = senha.sigla if senha.numero == 0 else f"{senha.sigla}{str(senha.numero).zfill(4)}"
        return jsonify({
            'senha': senha_completa,
            'guiche': senha.guiche or '...',
            'chamado_em': senha.chamado_em.isoformat() if senha.chamado_em else None,
            'id': senha.id
        })
    return jsonify({'senha': '', 'guiche': '...', 'chamado_em': None, 'id': None})

@bp.route('/tts_audio')
def tts_audio():
    # captura o texto da querystring
    texto = request.args.get('texto', '').strip()
    if not texto:
        return jsonify({'erro': 'Texto não fornecido'}), 400

    # pega a voz configurada (ou default)
    config = ConfiguracaoSistema.query.first()
    nome_voz = config.voz_azure if config and config.voz_azure else 'pt-BR-FranciscaNeural'

    # gera o áudio via Azure
    audio_data = gerar_audio_azure(texto, nome_voz)

    # devolve o MP3 diretamente
    return send_file(BytesIO(audio_data), mimetype='audio/mpeg')



@bp.route('/api/falar', methods=['POST'])
@login_required
def api_falar():
    texto = request.json.get('texto', '').strip()
    if not texto:
        return jsonify({'erro': 'Texto vazio'}), 400

    AZURE_TTS_KEY = '1GrRULjTQvppqKpUK2GSKc6YRwmdNdlDW4YywGXMfL6LkpfPU004JQQJ99BDACZoyfiXJ3w3AAAYACOGsj0S'
    AZURE_TTS_ENDPOINT = 'https://brazilsouth.api.cognitive.microsoft.com/'

    tts_url = f"{AZURE_TTS_ENDPOINT}cognitiveservices/v1"
    headers = {
        'Ocp-Apim-Subscription-Key': AZURE_TTS_KEY,
        'Content-Type': 'application/ssml+xml',
        'X-Microsoft-OutputFormat': 'audio-16khz-128kbitrate-mono-mp3',
    }

    ssml = f"""
    <speak version='1.0' xml:lang='pt-BR'>
        <voice name='pt-BR-FranciscaNeural'>{texto}</voice>
    </speak>
    """

    response = requests.post(tts_url, headers=headers, data=ssml.encode('utf-8'))
    if response.status_code != 200:
        return jsonify({'erro': 'Erro ao gerar áudio'}), 500

    return send_file(BytesIO(response.content), mimetype='audio/mpeg')

@bp.route('/api/tts', methods=['POST'])
def api_tts():
    from .models import ConfiguracaoSistema  # se ainda não estiver importado no topo

    dados = request.get_json()
    texto = dados.get('texto', '')

    if not texto:
        return jsonify({'erro': 'Texto não fornecido'}), 400

    try:
        config = ConfiguracaoSistema.query.first()
        nome_voz = config.voz_azure if config and config.voz_azure else 'pt-BR-FranciscaNeural'

        audio_data = gerar_audio_azure(texto, nome_voz)
        return send_file(BytesIO(audio_data), mimetype='audio/mpeg')
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@bp.route('/prisetup')
@login_required
@role_required('admin')
def prioridade_senhas():
    config = ConfiguracaoSistema.query.first()
    return render_template('PriSenhas.html', config=config)

@bp.route('/salvar_prioridade', methods=['POST'])
@login_required
@role_required('admin')
def salvar_prioridade():
    config = ConfiguracaoSistema.query.first()
    if not config:
        flash("Configuração do sistema não encontrada.")
        return redirect(url_for('main.edtelas'))

    tipo = request.form.get('tipo_prioridade')
    config.tipo_prioridade = tipo

    if tipo == 'intercalamento':
        valor = int(request.form.get('intercalamento_valor', 2))
        config.intercalamento_valor = valor

    elif tipo == 'peso':
        config.peso_normal = int(request.form.get('peso_normal', 1))
        config.peso_preferencial = int(request.form.get('peso_preferencial', 3))

    elif tipo == 'alternancia':
        config.tolerancia_minutos = int(request.form.get('tolerancia_minutos', 5))

    db.session.commit()
    flash("Configuração de prioridade salva com sucesso!")
    return redirect(url_for('main.prioridade_senhas'))


@bp.route('/painel_fila_json')
@login_required
@role_required('admin', 'usuario')
def painel_fila_json():
    senhas = (
        Senha.query
        .order_by(
            Senha.chamado.asc(),
            Senha.chamado_em.desc().nullslast(),
            Senha.id.asc()
        )
        .limit(15)
        .all()
    )
    return jsonify([{
        'id': s.id,
        # se número for 0 (chamada personalizada), mostra só a sigla
        'senha_completa': s.sigla if s.numero == 0 else f"{s.sigla}{str(s.numero).zfill(4)}",
        'chamado': s.chamado,
        'chamado_por': s.chamado_por,
        'chamado_em': s.chamado_em.isoformat() if s.chamado_em else None,
        'numero': s.numero,
    } for s in senhas])


@bp.route('/api/painel_action', methods=['POST'])
@login_required
@role_required('admin', 'usuario')
def painel_action():
    from datetime import datetime
    from flask import abort

    data = request.get_json(force=True)
    acao   = data.get('acao')
    guiche = data.get('guiche', session.get('guiche','')).strip()

    # valida guichê
    if not guiche:
        return jsonify({'success': False, 'error': 'Guichê não informado.'}), 400
    session['guiche'] = guiche

    # ─── PERSONALIZADA ────────────────────────────────────
    if acao == 'personalizada':
        texto = data.get('texto_personalizado','').strip()
        if not texto:
            return jsonify({'success': False, 'error': 'Texto não fornecido.'}), 400
        nova = Senha(
            sigla=texto,
            numero=0,
            chamado=True,
            chamado_por=current_user.id,
            chamado_em=datetime.utcnow(),
            guiche=guiche,
            tipo_paciente='normal',
            primeira_vez=False
        )
        db.session.add(nova)
        db.session.commit()
        msg = f"📣 Chamada personalizada: {texto}"
        session['mensagem_voz'] = f"{texto}, dirija-se ao guichê {guiche}"
        flash(msg)
        return jsonify({'success': True, 'message': msg})

    # ─── PRÓXIMA SENHA ────────────────────────────────────
    elif acao == 'proxima':
        # aqui copiamos a lógica de main.chamar_senha, mas devolvendo JSON:
        config = ConfiguracaoSistema.query.first()
        # — seletores internos —
        def sel_pref(): return Senha.query.filter_by(chamado=False, tipo_paciente='preferencial').order_by(Senha.id).first()
        def sel_norm(): return Senha.query.filter_by(chamado=False, tipo_paciente='normal').order_by(Senha.id).first()

        senha = None
        # intercalamento
        if config.tipo_prioridade == 'intercalamento':
            cnt = session.get('contador_normais',0)
            val = config.intercalamento_valor or 2
            if cnt >= val:
                senha = sel_pref()
                session['contador_normais'] = 0
            else:
                senha = sel_norm()
                session['contador_normais'] = cnt + 1
            if not senha:
                senha = sel_pref() or sel_norm()

        # peso
        elif config.tipo_prioridade == 'peso':
            pesos = []
            opcoes = []
            if Senha.query.filter_by(chamado=False, tipo_paciente='normal').count():
                opcoes.append('normal'); pesos.append(config.peso_normal or 1)
            if Senha.query.filter_by(chamado=False, tipo_paciente='preferencial').count():
                opcoes.append('preferencial'); pesos.append(config.peso_preferencial or 3)
            from random import choices
            if opcoes:
                tipo = choices(opcoes, pesos, k=1)[0]
                senha = sel_norm() if tipo=='normal' else sel_pref()
                if not senha:
                    senha = sel_pref() if tipo=='normal' else sel_norm()

        # alternância
        else:
            toler = config.tolerancia_minutos or 5
            agora = datetime.utcnow()
            pref   = Senha.query.filter_by(chamado=False, tipo_paciente='preferencial').order_by(Senha.id).all()
            norm   = Senha.query.filter_by(chamado=False, tipo_paciente='normal').order_by(Senha.id).all()
            ultima_pref = Senha.query.filter_by(chamado=True, tipo_paciente='preferencial').order_by(Senha.chamado_em.desc()).first()
            espera = ((agora - ultima_pref.chamado_em).total_seconds()/60) if ultima_pref and ultima_pref.chamado_em else toler+1
            if espera > toler:
                senha = pref[0] if pref else (norm[0] if norm else None)
            else:
                senha = norm[0] if norm else (pref[0] if pref else None)

        if not senha:
            return jsonify({'success': False, 'error': 'Nenhuma senha na fila.'}), 400

        senha.chamado     = True
        senha.chamado_por = current_user.id
        senha.chamado_em  = datetime.utcnow()
        senha.guiche      = guiche
        db.session.commit()

        msg = f"📢 Próxima senha: Senha {senha.sigla}{str(senha.numero).zfill(4)}, dirija-se ao guichê {guiche}"
        session['mensagem_voz'] = f"Senha {senha.sigla}{str(senha.numero).zfill(4)}, dirija-se ao guichê {guiche}"
        flash(msg)
        return jsonify({'success': True, 'message': msg})

    # ─── RECHAMAR ───────────────────────────────────────────
    elif acao == 'rechamar':
        id_r = data.get('rechamar_id')
        senha = Senha.query.get(id_r)
        if not senha:
            return jsonify({'success': False, 'error': 'Senha não encontrada.'}), 404
        senha.chamado_em   = datetime.utcnow()
        senha.guiche       = guiche
        senha.chamado_por  = current_user.id
        db.session.commit()
        msg = f"🔁 Rechamada manual: Senha {senha.sigla}{str(senha.numero).zfill(4)}"
        session['mensagem_voz'] = f"Senha {senha.sigla}{str(senha.numero).zfill(4)}, dirija-se ao guichê {guiche}"
        flash(msg)
        return jsonify({'success': True, 'message': msg})

    # ─── AÇÃO INVÁLIDA ─────────────────────────────────────
    return jsonify({'success': False, 'error': 'Ação inválida.'}), 400


@bp.route('/api/painel_action', methods=['POST'])
@login_required
@role_required('admin', 'usuario')
def painel_action_api():
    from datetime import datetime
    from flask import request, jsonify, session
    from .models import Senha, ConfiguracaoSistema
    from . import db

    data   = request.get_json(force=True) or {}
    acao   = data.get('acao')
    guiche = data.get('guiche', session.get('guiche', '')).strip()

    if not guiche:
        return jsonify(success=False, message="Informe o número do guichê."), 400
    session['guiche'] = guiche

    # ─── PERSONALIZADA ────────────────────────────────────
    if acao == 'personalizada':
        # ... seu código existente ...
        pass

    # ─── PRÓXIMA SENHA ATÔMICA ─────────────────────────────
    elif acao == 'proxima':
        config = ConfiguracaoSistema.query.first()

        with db.session.begin():  # abre transação
            # bloqueia as linhas para evitar race conditions
            def sel_pref():
                return (db.session.query(Senha)
                                 .filter_by(chamado=False, tipo_paciente='preferencial')
                                 .order_by(Senha.id)
                                 .with_for_update()
                                 .first())

            def sel_norm():
                return (db.session.query(Senha)
                                 .filter_by(chamado=False, tipo_paciente='normal')
                                 .order_by(Senha.id)
                                 .with_for_update()
                                 .first())

            senha = None
            # intercalamento
            if config.tipo_prioridade == 'intercalamento':
                cnt = session.get('contador_normais', 0)
                val = config.intercalamento_valor or 2
                if cnt >= val:
                    senha = sel_pref()
                    session['contador_normais'] = 0
                else:
                    senha = sel_norm()
                    session['contador_normais'] = cnt + 1
                if not senha:
                    senha = sel_pref() or sel_norm()

            # peso
            elif config.tipo_prioridade == 'peso':
                from random import choices
                opcoes, pesos = [], []
                if Senha.query.filter_by(chamado=False, tipo_paciente='normal').count():
                    opcoes.append('normal'); pesos.append(config.peso_normal or 1)
                if Senha.query.filter_by(chamado=False, tipo_paciente='preferencial').count():
                    opcoes.append('preferencial'); pesos.append(config.peso_preferencial or 3)
                if opcoes:
                    tipo = choices(opcoes, pesos, k=1)[0]
                    senha = sel_norm() if tipo == 'normal' else sel_pref()
                    if not senha:
                        senha = sel_pref() if tipo == 'normal' else sel_norm()

            # alternância
            else:
                toler = config.tolerancia_minutos or 5
                agora = datetime.utcnow()
                pref = Senha.query.filter_by(chamado=False, tipo_paciente='preferencial').order_by(Senha.id).all()
                norm = Senha.query.filter_by(chamado=False, tipo_paciente='normal').order_by(Senha.id).all()
                ultima_pref = (Senha.query
                                  .filter_by(chamado=True, tipo_paciente='preferencial')
                                  .order_by(Senha.chamado_em.desc())
                                  .first())
                espera = ((agora - ultima_pref.chamado_em).total_seconds()/60) \
                         if ultima_pref and ultima_pref.chamado_em else toler + 1
                if espera > toler:
                    senha = pref[0] if pref else (norm[0] if norm else None)
                else:
                    senha = norm[0] if norm else (pref[0] if pref else None)

            if not senha:
                return jsonify(success=False, message="Nenhuma senha na fila."), 400

            # marca e comita dentro da mesma transação
            senha.chamado     = True
            senha.chamado_por = current_user.id
            senha.chamado_em  = datetime.utcnow()
            senha.guiche      = guiche
            db.session.flush()  # atualiza antes do commit automático

        # aqui a transação já foi committed e desbloqueada
        completo = senha.sigla if senha.numero == 0 else f"{senha.sigla}{str(senha.numero).zfill(4)}"
        msg = f"📢 Próxima senha: {completo}, dirija-se ao guichê {guiche}"
        return jsonify(success=True, message=msg)

    # ─── RECHAMAR ───────────────────────────────────────────
    elif acao == 'rechamar':
        # ... seu código existente ...
        pass

    return jsonify(success=False, message="Ação inválida."), 400


@bp.route('/ping')
def ping():
    return '', 200
