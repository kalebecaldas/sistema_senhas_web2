from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify, session
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import os
from werkzeug.utils import secure_filename

from .models import Usuario, Senha, ConfiguracaoSistema
from . import db
from .auth_utils import role_required
from .services import PrioridadeService, ImpressoraService, TTSService

import requests
from flask import send_file
from io import BytesIO


bp = Blueprint("main", __name__)

from datetime import datetime, timedelta
from flask import g

@bp.before_request
def controlar_sessao_por_inatividade():
    # Log apenas para rotas importantes, não para APIs e polling
    rotas_importantes = {
        'main.login',
        'main.logout', 
        'main.painel',
        'main.usuarios',
        'main.cadastro',
        'main.editar_usuario',
        'main.edtelas',
        'main.prioridade_senhas',
        'main.relatorios',
        'main.relatorio_personalizado',
        'main.chamar_senha'
    }
    
    if request.endpoint in rotas_importantes:
        print(f"📌 Rota acessada: {request.endpoint}")
    
    g.endpoint = request.endpoint

    rotas_livres = {
        'main.retira_senha',
        'main.display',
        'main.gerar_senha_triada',
        'main.ping',
        'main.login',
        'main.fila_json',
        'main.ultima_chamada',
        'main.painel_fila_json',
        'main.api_retira_senha',
        'main.api_falar',
        'main.api_tts',
        'main.api_painel_action',
        'main.buscar_usuarios',
        'main.tts_audio'
    }

    if request.endpoint in rotas_livres:
        return

    if current_user.is_authenticated:
        session.permanent = True
        # ⏳ duração total da sessão - configurado no app principal

        agora = datetime.utcnow()
        ultimo_uso = session.get('ultimo_uso')

        if ultimo_uso:
            try:
                delta = agora - datetime.fromisoformat(ultimo_uso)
                if delta > timedelta(hours=8):  # ⏳ inatividade de 8h
                    logout_user()
                    session.clear()
                    flash("Sessão encerrada por inatividade.", "warning")
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
        flash('Login ou senha inválidos', 'error')
    config = ConfiguracaoSistema.query.first()
    return render_template('login.html', config=config)

@bp.route('/retira')
def retira_senha():
    config = ConfiguracaoSistema.query.first()
    return render_template('gerar_senha.html', config=config, exibir_menu=False)


import socket


@bp.route('/api/retirar')
def api_retira_senha():
    from sqlalchemy.exc import SQLAlchemyError

    tipo_paciente = request.args.get('tipo', 'normal')
    sigla = 'NP' if tipo_paciente == 'normal' else 'PP'
    primeira_vez = False

    try:
        # Gerar número da senha
        ultima = Senha.query.order_by(Senha.id.desc()).first()
        numero = (ultima.numero + 1) if ultima else 1
        senha_completa = f"{sigla}{str(numero).zfill(4)}"

        # Criar senha no banco (sem commit ainda)
        nova = Senha(
            numero=numero, 
            sigla=sigla, 
            tipo_paciente=tipo_paciente, 
            primeira_vez=primeira_vez
        )
        db.session.add(nova)
        db.session.flush()

        # Imprimir usando serviço
        impressora = ImpressoraService()
        if not impressora.imprimir_senha(senha_completa, 'secundaria'):
            raise Exception("Falha na impressão")

        db.session.commit()  # só grava no banco após sucesso na impressão

        return jsonify({'numero': numero, 'sigla': sigla, 'primeira_vez': primeira_vez})

    except Exception as e:
        db.session.rollback()
        print('Erro ao imprimir ou salvar:', e)
        return jsonify({'erro': 'Erro ao imprimir. Senha não foi salva.'}), 500



@bp.route('/api/gerar_senha')
def gerar_senha_triada():
    from datetime import datetime, time
    from sqlalchemy.exc import SQLAlchemyError

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

    try:
        # Gerar número da senha
        agora = datetime.now()
        inicio_dia = datetime.combine(agora.date(), time.min)
        count = Senha.query.filter(Senha.gerado_em >= inicio_dia).count()
        numero = count + 1
        senha_completa = f"{sigla}{str(numero).zfill(4)}"

        # Imprimir usando serviço
        impressora = ImpressoraService()
        if not impressora.imprimir_senha(senha_completa, 'principal'):
            raise Exception("Falha na impressão")

        # Só salva se imprimir com sucesso
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

        return jsonify({
            'sigla': sigla,
            'numero': numero,
            'completo': senha_completa
        })

    except Exception as e:
        db.session.rollback()
        print('Erro ao imprimir ou salvar:', e)
        return jsonify({'erro': 'Erro ao imprimir. Senha não foi salva.'}), 500

@bp.route('/display')
def display():
    senhas = Senha.query.filter_by(chamado=True).order_by(Senha.id.desc()).limit(15).all()
    config = ConfiguracaoSistema.query.first()
    return render_template('display.html', senhas=senhas, config=config, exibir_menu=False)

@bp.route('/fila_json')
def fila_json():
    senhas = Senha.query.filter_by(chamado=True).order_by(Senha.id.desc()).all()
    dados = [{
        'id': s.id,
        'sigla': s.sigla,
        'numero': s.numero,
        'chamado': s.chamado,
        'chamado_em': s.chamado_em.isoformat() if s.chamado_em else None,
        'senha_completa': s.sigla if s.numero == 0 else f"{s.sigla}{str(s.numero).zfill(4)}",
        'guiche': s.guiche or ''
    } for s in senhas]

    versao = max([s.chamado_em or s.gerado_em for s in senhas], default=datetime.utcnow()).isoformat()
    return jsonify({'versao': versao, 'senhas': dados})


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

    config = ConfiguracaoSistema.query.first()
    guiche = request.args.get("guiche") or session.get("guiche") or ""
    session['guiche'] = guiche

    if not guiche:
        flash("Informe o número do guichê antes de realizar chamadas.")
        return redirect(url_for('main.painel'))

    # Usar serviço de prioridade
    prioridade_service = PrioridadeService(db.session, config)
    contador_normais = session.get('contador_normais', 0)
    
    senha, novo_contador = prioridade_service.selecionar_proxima_senha(contador_normais)
    
    if senha:
        senha.chamado = True
        senha.chamado_por = current_user.id
        senha.chamado_em = datetime.utcnow()
        senha.guiche = guiche
        db.session.commit()
        
        # Atualizar contador na sessão
        session['contador_normais'] = novo_contador
        
        # Formatar mensagem de voz
        tts_service = TTSService(config)
        senha_completa = f"{senha.sigla}{str(senha.numero).zfill(4)}"
        mensagem_voz = tts_service.formatar_mensagem_voz(senha_completa, guiche)
        session['mensagem_voz'] = mensagem_voz
        
        flash(mensagem_voz)
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
        flash('Usuário atualizado com sucesso.', 'success')
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
            flash('Este e-mail já está cadastrado.', 'error')
            return redirect(url_for('main.cadastro'))

        novo = Usuario(
            nome=nome,
            email=email,
            senha=generate_password_hash(senha),
            tipo=tipo
        )
        db.session.add(novo)
        db.session.commit()
        flash('Usuário cadastrado com sucesso!', 'success')
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

# Rota /tts_audio movida para tts_routes.py



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
    dados = request.get_json()
    texto = dados.get('texto', '')

    if not texto:
        return jsonify({'erro': 'Texto não fornecido'}), 400

    try:
        config = ConfiguracaoSistema.query.first()
        if not config:
            return jsonify({'erro': 'Configuração não encontrada'}), 500

        tts_service = TTSService(config)
        audio_data = tts_service.gerar_audio(texto)
        return send_file(BytesIO(audio_data), mimetype='audio/mpeg')
    except Exception as e:
        return jsonify({'erro': str(e)}), 500


@bp.route('/teste-tts')
def teste_tts():
    return render_template('teste_tts.html')

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

    data = request.get_json(force=True)
    acao   = data.get('acao')
    guiche = data.get('guiche', session.get('guiche','')).strip()

    if not guiche:
        return jsonify({'success': False, 'error': 'Guichê não informado.'}), 400
    session['guiche'] = guiche

    config = ConfiguracaoSistema.query.first()
    tts_service = TTSService(config)

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
        
        mensagem_voz = tts_service.formatar_mensagem_voz(texto, guiche)
        session['mensagem_voz'] = mensagem_voz
        return jsonify({'success': True, 'message': f"📣 Chamada personalizada: {texto}"})

    elif acao == 'proxima':
        # Usar serviço de prioridade
        prioridade_service = PrioridadeService(db.session, config)
        contador_normais = session.get('contador_normais', 0)
        
        senha, novo_contador = prioridade_service.selecionar_proxima_senha(contador_normais)
        
        if not senha:
            return jsonify({'success': False, 'message': 'Nenhuma senha na fila.'}), 400

        senha.chamado = True
        senha.chamado_por = current_user.id
        senha.chamado_em = datetime.utcnow()
        senha.guiche = guiche
        db.session.commit()
        
        # Atualizar contador na sessão
        session['contador_normais'] = novo_contador

        completo = senha.sigla if senha.numero == 0 else f"{senha.sigla}{str(senha.numero).zfill(4)}"
        mensagem_voz = tts_service.formatar_mensagem_voz(completo, guiche)
        session['mensagem_voz'] = mensagem_voz
        
        return jsonify({'success': True, 'message': f"📢 Próxima senha: {completo}, dirija-se ao guichê {guiche}"})

    elif acao == 'rechamar':
        id_r = data.get('rechamar_id')
        senha = Senha.query.get(id_r)
        if not senha:
            return jsonify({'success': False, 'error': 'Senha não encontrada.'}), 404
        
        senha.chamado_em = datetime.utcnow()
        senha.guiche = guiche
        senha.chamado_por = current_user.id
        db.session.commit()
        
        completo = senha.sigla if senha.numero == 0 else f"{senha.sigla}{str(senha.numero).zfill(4)}"
        mensagem_voz = tts_service.formatar_mensagem_voz(completo, guiche)
        session['mensagem_voz'] = mensagem_voz
        
        return jsonify({'success': True, 'message': f"🔁 Rechamada manual: Senha {completo}"})

    return jsonify({'success': False, 'message': 'Ação inválida.'}), 400




@bp.route('/ping')
def ping():
    return '', 200

# ============================================================================
# SISTEMA DE ATUALIZAÇÃO
# ============================================================================

@bp.route('/atualizacoes')
@login_required
@role_required('admin')  # Apenas administradores podem acessar
def atualizacoes():
    """Página de atualizações do sistema"""
    from app.version import version_manager
    
    system_info = version_manager.get_system_info()
    
    return render_template('atualizacoes.html', 
                         config=ConfiguracaoSistema.query.first(),
                         system_info=system_info)

@bp.route('/api/check_updates')
@login_required
@role_required('admin')  # Apenas administradores podem verificar
def api_check_updates():
    """API para verificar atualizações"""
    from app.version import version_manager
    
    update_info = version_manager.check_for_updates()
    return jsonify(update_info)

@bp.route('/api/update_system', methods=['POST'])
@login_required
@role_required('admin')  # Apenas administradores podem atualizar
def api_update_system():
    """API para atualizar o sistema"""
    from app.version import version_manager
    
    # Log da tentativa de atualização
    print(f"🔄 Tentativa de atualização por: {current_user.email} ({current_user.tipo})")
    
    result = version_manager.update_system()
    
    # Log do resultado
    if result.get('success'):
        print(f"✅ Atualização bem-sucedida por: {current_user.email}")
    else:
        print(f"❌ Falha na atualização por: {current_user.email} - {result.get('error', 'Erro desconhecido')}")
    
    return jsonify(result)

# ============================================================================
# RELATÓRIOS E DASHBOARD
# ============================================================================

@bp.route('/limpar_dados_teste', methods=['POST'])
@login_required
def limpar_dados_teste():
    """Limpar dados antigos de teste do banco de dados"""
    from datetime import datetime, timedelta
    
    try:
        # Definir data limite (7 dias atrás)
        data_limite = datetime.now() - timedelta(days=7)
        
        # Contar senhas que serão removidas
        senhas_para_remover = Senha.query.filter(
            Senha.gerado_em < data_limite
        ).count()
        
        # Remover senhas antigas
        Senha.query.filter(
            Senha.gerado_em < data_limite
        ).delete()
        
        db.session.commit()
        
        flash(f'Removidas {senhas_para_remover} senhas antigas (anteriores a {data_limite.strftime("%d/%m/%Y")})', 'success')
        
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao limpar dados: {str(e)}', 'danger')
    
    return redirect(url_for('main.relatorios'))

@bp.route('/relatorios')
@login_required
def relatorios():
    """Página principal de relatórios com dashboard"""
    config = ConfiguracaoSistema.query.first()
    
    # Estatísticas gerais
    total_senhas = Senha.query.count()
    senhas_chamadas = Senha.query.filter_by(chamado=True).count()
    senhas_aguardando = Senha.query.filter_by(chamado=False).count()
    
    # Por tipo de paciente
    normais = Senha.query.filter_by(tipo_paciente='normal').count()
    preferenciais = Senha.query.filter_by(tipo_paciente='preferencial').count()
    
    # Por primeira vez
    primeira_vez = Senha.query.filter_by(primeira_vez=True).count()
    recorrentes = Senha.query.filter_by(primeira_vez=False).count()
    
    # Por usuário que chamou
    chamadas_por_usuario = db.session.query(
        Usuario.nome,
        db.func.count(Senha.id).label('total_chamadas')
    ).join(Senha, Usuario.id == Senha.chamado_por)\
     .filter(Senha.chamado == True)\
     .group_by(Usuario.id, Usuario.nome)\
     .order_by(db.func.count(Senha.id).desc())\
     .all()
    
    # Senhas por dia (últimos 30 dias)
    from datetime import datetime, timedelta
    hoje = datetime.now().date()
    senhas_por_dia = []
    
    # Buscar dados dos últimos 30 dias
    for i in range(30):
        data = hoje - timedelta(days=i)
        count = Senha.query.filter(
            db.func.date(Senha.gerado_em) == data
        ).count()
        if count > 0:  # Só incluir dias com senhas
            senhas_por_dia.append({
                'data': data,
                'total': count
            })
    
    # Ordenar por data (mais antiga primeiro)
    senhas_por_dia.sort(key=lambda x: x['data'])
    
    # Tempo médio de espera (senhas chamadas nos últimos 30 dias)
    tempo_medio = None
    data_limite = datetime.now() - timedelta(days=30)
    senhas_chamadas_validas = Senha.query.filter(
        Senha.chamado == True,
        Senha.chamado_em != None,
        Senha.gerado_em != None,
        Senha.chamado_em > Senha.gerado_em,
        Senha.gerado_em >= data_limite  # Apenas senhas dos últimos 30 dias
    ).all()
    if senhas_chamadas_validas:
        tempos = [
            (s.chamado_em - s.gerado_em).total_seconds() / 60
            for s in senhas_chamadas_validas
        ]
        # Filtrar tempos muito altos (acima de 2 horas) que podem ser dados de teste
        tempos_filtrados = [t for t in tempos if t <= 120]  # Máximo 2 horas
        if tempos_filtrados:
            tempo_medio = round(sum(tempos_filtrados) / len(tempos_filtrados), 1)
    
    return render_template('relatorios.html', 
                         config=config,
                         total_senhas=total_senhas,
                         senhas_chamadas=senhas_chamadas,
                         senhas_aguardando=senhas_aguardando,
                         normais=normais,
                         preferenciais=preferenciais,
                         primeira_vez=primeira_vez,
                         recorrentes=recorrentes,
                         chamadas_por_usuario=chamadas_por_usuario,
                         senhas_por_dia=senhas_por_dia,
                         tempo_medio=tempo_medio)

@bp.route('/relatorio_personalizado')
@login_required
def relatorio_personalizado():
    """Página para criar relatórios personalizados"""
    config = ConfiguracaoSistema.query.first()
    
    # Buscar dados para filtros
    usuarios = Usuario.query.all()
    tipos_paciente = db.session.query(Senha.tipo_paciente).distinct().all()
    
    # Calcular estatísticas rápidas
    total_senhas = Senha.query.count()
    senhas_chamadas = Senha.query.filter_by(chamado=True).count()
    senhas_aguardando = Senha.query.filter_by(chamado=False).count()
    
    return render_template('relatorio_personalizado.html', 
                         config=config,
                         usuarios=usuarios,
                         tipos_paciente=tipos_paciente,
                         total_senhas=total_senhas,
                         senhas_chamadas=senhas_chamadas,
                         senhas_aguardando=senhas_aguardando)

@bp.route('/gerar_relatorio', methods=['POST'])
@login_required
def gerar_relatorio():
    """Gerar relatório personalizado em PDF ou Excel"""
    from datetime import datetime, timedelta
    import json
    
    # Obter parâmetros do formulário
    formato = request.form.get('formato', 'pdf')
    data_inicio = request.form.get('data_inicio')
    data_fim = request.form.get('data_fim')
    tipo_paciente = request.form.get('tipo_paciente')
    primeira_vez = request.form.get('primeira_vez')
    usuario_id = request.form.get('usuario_id')
    chamadas_apenas = request.form.get('chamadas_apenas') == 'on'
    
    # Construir query base
    query = Senha.query
    
    # Aplicar filtros
    if data_inicio:
        query = query.filter(Senha.gerado_em >= datetime.strptime(data_inicio, '%Y-%m-%d'))
    if data_fim:
        query = query.filter(Senha.gerado_em <= datetime.strptime(data_fim, '%Y-%m-%d') + timedelta(days=1))
    if tipo_paciente:
        query = query.filter(Senha.tipo_paciente == tipo_paciente)
    if primeira_vez:
        query = query.filter(Senha.primeira_vez == (primeira_vez == 'true'))
    if usuario_id:
        query = query.filter(Senha.chamado_por == usuario_id)
    if chamadas_apenas:
        query = query.filter(Senha.chamado == True)
    
    # Executar query
    senhas = query.order_by(Senha.gerado_em.desc()).all()
    
    # Gerar relatório
    if formato == 'pdf':
        return gerar_pdf_relatorio(senhas, request.form)
    else:
        return gerar_excel_relatorio(senhas, request.form)

def gerar_pdf_relatorio(senhas, parametros):
    """Gerar relatório em PDF com formatação melhorada e totais"""
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.lib import colors
    from io import BytesIO
    from datetime import datetime
    from collections import defaultdict
    
    # Criar buffer para o PDF
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=1*inch, bottomMargin=1*inch)
    elements = []
    
    # Estilos
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        spaceAfter=30,
        alignment=1,  # Centralizado
        fontName='Helvetica-Bold'
    )
    
    subtitle_style = ParagraphStyle(
        'Subtitle',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=20,
        alignment=1,
        fontName='Helvetica-Bold'
    )
    
    section_style = ParagraphStyle(
        'Section',
        parent=styles['Heading3'],
        fontSize=12,
        spaceAfter=15,
        fontName='Helvetica-Bold'
    )
    
    # ============================================================================
    # CABEÇALHO DO RELATÓRIO
    # ============================================================================
    elements.append(Paragraph("SISTEMA DE SENHAS - IAAM", title_style))
    elements.append(Paragraph("RELATÓRIO PERSONALIZADO", subtitle_style))
    elements.append(Spacer(1, 20))
    
    # ============================================================================
    # INFORMAÇÕES DO RELATÓRIO
    # ============================================================================
    elements.append(Paragraph("INFORMAÇÕES DO RELATÓRIO", section_style))
    
    info_data = [
        ['Gerado em:', datetime.now().strftime('%d/%m/%Y às %H:%M:%S')],
        ['Gerado por:', current_user.nome],
        ['Total de registros:', str(len(senhas))],
    ]
    
    # Adicionar filtros aplicados
    filtros_aplicados = []
    if parametros.get('data_inicio'):
        filtros_aplicados.append(f"De {parametros['data_inicio']}")
    if parametros.get('data_fim'):
        filtros_aplicados.append(f"Até {parametros['data_fim']}")
    if parametros.get('tipo_paciente'):
        tipo = 'Preferencial' if parametros['tipo_paciente'] == 'preferencial' else 'Normal'
        filtros_aplicados.append(f"Tipo: {tipo}")
    if parametros.get('primeira_vez'):
        vez = 'Primeira vez' if parametros['primeira_vez'] == 'true' else 'Recorrentes'
        filtros_aplicados.append(f"Categoria: {vez}")
    if parametros.get('usuario_id'):
        usuario = Usuario.query.get(parametros['usuario_id'])
        if usuario:
            filtros_aplicados.append(f"Usuário: {usuario.nome}")
    if parametros.get('chamadas_apenas') == 'on':
        filtros_aplicados.append("Apenas senhas chamadas")
    
    if filtros_aplicados:
        info_data.append(['Filtros aplicados:', ', '.join(filtros_aplicados)])
    
    info_table = Table(info_data, colWidths=[2*inch, 4*inch])
    info_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('ALIGN', (1, 0), (1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    elements.append(info_table)
    elements.append(Spacer(1, 30))
    
    # ============================================================================
    # RESUMO ESTATÍSTICO
    # ============================================================================
    if senhas:
        elements.append(Paragraph("RESUMO ESTATÍSTICO", section_style))
        
        # Calcular estatísticas
        total_senhas = len(senhas)
        senhas_normais = len([s for s in senhas if s.tipo_paciente == 'normal'])
        senhas_preferenciais = len([s for s in senhas if s.tipo_paciente == 'preferencial'])
        primeira_vez = len([s for s in senhas if s.primeira_vez])
        recorrentes = len([s for s in senhas if not s.primeira_vez])
        senhas_chamadas = len([s for s in senhas if s.chamado])
        senhas_aguardando = len([s for s in senhas if not s.chamado])
        
        # Estatísticas por tipo
        stats_data = [
            ['CATEGORIA', 'QUANTIDADE', 'PERCENTUAL'],
            ['Total de Senhas', str(total_senhas), '100%'],
            ['Senhas Normais', str(senhas_normais), f"{senhas_normais/total_senhas*100:.1f}%" if total_senhas > 0 else '0%'],
            ['Senhas Preferenciais', str(senhas_preferenciais), f"{senhas_preferenciais/total_senhas*100:.1f}%" if total_senhas > 0 else '0%'],
            ['Primeira Vez', str(primeira_vez), f"{primeira_vez/total_senhas*100:.1f}%" if total_senhas > 0 else '0%'],
            ['Recorrentes', str(recorrentes), f"{recorrentes/total_senhas*100:.1f}%" if total_senhas > 0 else '0%'],
            ['Chamadas', str(senhas_chamadas), f"{senhas_chamadas/total_senhas*100:.1f}%" if total_senhas > 0 else '0%'],
            ['Aguardando', str(senhas_aguardando), f"{senhas_aguardando/total_senhas*100:.1f}%" if total_senhas > 0 else '0%'],
        ]
        
        stats_table = Table(stats_data, colWidths=[2.5*inch, 1.5*inch, 1.5*inch])
        stats_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.lightblue),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
        ]))
        elements.append(stats_table)
        elements.append(Spacer(1, 30))
        
        # ============================================================================
        # CHAMADAS POR USUÁRIO
        # ============================================================================
        elements.append(Paragraph("CHAMADAS POR USUÁRIO", section_style))
        
        # Calcular chamadas por usuário
        chamadas_por_usuario = defaultdict(int)
        for senha in senhas:
            if senha.chamado and senha.usuario_chamador:
                chamadas_por_usuario[senha.usuario_chamador.nome] += 1
        
        if chamadas_por_usuario:
            user_data = [['USUÁRIO', 'TOTAL DE CHAMADAS', 'PERCENTUAL']]
            for usuario, total in sorted(chamadas_por_usuario.items(), key=lambda x: x[1], reverse=True):
                percentual = f"{total/senhas_chamadas*100:.1f}%" if senhas_chamadas > 0 else '0%'
                user_data.append([usuario, str(total), percentual])
            
            user_table = Table(user_data, colWidths=[3*inch, 1.5*inch, 1.5*inch])
            user_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.darkgreen),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 11),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.lightgreen),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('FONTSIZE', (0, 1), (-1, -1), 10),
                ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
            ]))
            elements.append(user_table)
        else:
            elements.append(Paragraph("Nenhuma chamada registrada no período.", styles['Normal']))
        
        elements.append(Spacer(1, 30))
        
        # ============================================================================
        # DADOS DETALHADOS DAS SENHAS
        # ============================================================================
        elements.append(Paragraph("DADOS DETALHADOS DAS SENHAS", section_style))
        
        # Cabeçalho da tabela
        data = [['Nº', 'TIPO', '1ª VEZ', 'GERADO EM', 'CHAMADO', 'CHAMADO POR', 'GUICHÊ', 'TEMPO ESPERA']]
        
        for senha in senhas:
            chamado_por = senha.usuario_chamador.nome if senha.usuario_chamador else 'Não chamado'
            gerado_em = senha.gerado_em.strftime('%d/%m %H:%M')
            
            # Calcular tempo de espera
            tempo_espera = '-'
            if senha.chamado and senha.chamado_em and senha.gerado_em:
                diff = senha.chamado_em - senha.gerado_em
                minutos = int(diff.total_seconds() / 60)
                # Validar se o tempo é razoável (máximo 2 horas)
                if 0 <= minutos <= 120:
                    tempo_espera = f"{minutos}min"
                else:
                    tempo_espera = "Inválido"
            
            data.append([
                f"{senha.sigla}{senha.numero:03d}",
                'Pref' if senha.tipo_paciente == 'preferencial' else 'Norm',
                'Sim' if senha.primeira_vez else 'Não',
                gerado_em,
                'Sim' if senha.chamado else 'Não',
                chamado_por[:15] + '...' if len(chamado_por) > 15 else chamado_por,
                senha.guiche or '-',
                tempo_espera
            ])
        
        # Criar tabela com larguras ajustadas
        table = Table(data, colWidths=[0.7*inch, 0.6*inch, 0.5*inch, 1*inch, 0.6*inch, 1.5*inch, 0.6*inch, 0.8*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkgrey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 9),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.beige, colors.white]),
        ]))
        elements.append(table)
    else:
        elements.append(Paragraph("Nenhum registro encontrado com os filtros aplicados.", styles['Normal']))
    
    # ============================================================================
    # RODAPÉ
    # ============================================================================
    elements.append(Spacer(1, 30))
    elements.append(Paragraph(f"Relatório gerado automaticamente pelo Sistema de Senhas IAAM em {datetime.now().strftime('%d/%m/%Y às %H:%M:%S')}", 
                             ParagraphStyle('Footer', parent=styles['Normal'], fontSize=8, alignment=1)))
    
    # Gerar PDF
    doc.build(elements)
    buffer.seek(0)
    
    # Retornar arquivo
    from flask import send_file
    return send_file(
        buffer,
        as_attachment=True,
        download_name=f'relatorio_senhas_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf',
        mimetype='application/pdf'
    )

def gerar_excel_relatorio(senhas, parametros):
    """Gerar relatório em Excel com formatação melhorada e totais"""
    import pandas as pd
    from io import BytesIO
    from datetime import datetime
    from collections import defaultdict
    
    # Preparar dados detalhados
    dados = []
    for senha in senhas:
        # Calcular tempo de espera
        tempo_espera = '-'
        if senha.chamado and senha.chamado_em and senha.gerado_em:
            diff = senha.chamado_em - senha.gerado_em
            minutos = int(diff.total_seconds() / 60)
            # Validar se o tempo é razoável (máximo 2 horas)
            if 0 <= minutos <= 120:
                tempo_espera = f"{minutos} minutos"
            else:
                tempo_espera = "Inválido"
        
        dados.append({
            'Número': f"{senha.sigla}{senha.numero:03d}",
            'Tipo': 'Preferencial' if senha.tipo_paciente == 'preferencial' else 'Normal',
            'Primeira Vez': 'Sim' if senha.primeira_vez else 'Não',
            'Gerado em': senha.gerado_em.strftime('%d/%m/%Y %H:%M'),
            'Chamado': 'Sim' if senha.chamado else 'Não',
            'Chamado em': senha.chamado_em.strftime('%d/%m/%Y %H:%M') if senha.chamado_em else 'Não chamado',
            'Chamado por': senha.usuario_chamador.nome if senha.usuario_chamador else 'Não chamado',
            'Guichê': senha.guiche or '-',
            'Tempo de Espera': tempo_espera
        })
    
    # Criar DataFrame
    df = pd.DataFrame(dados)
    
    # Criar buffer para Excel
    buffer = BytesIO()
    
    # Criar Excel com múltiplas abas
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        # ============================================================================
        # ABA 1: DADOS DETALHADOS
        # ============================================================================
        df.to_excel(writer, sheet_name='Dados Detalhados', index=False)
        
        # ============================================================================
        # ABA 2: INFORMAÇÕES DO RELATÓRIO
        # ============================================================================
        # Adicionar filtros aplicados
        filtros_aplicados = []
        if parametros.get('data_inicio'):
            filtros_aplicados.append(f"De {parametros['data_inicio']}")
        if parametros.get('data_fim'):
            filtros_aplicados.append(f"Até {parametros['data_fim']}")
        if parametros.get('tipo_paciente'):
            tipo = 'Preferencial' if parametros['tipo_paciente'] == 'preferencial' else 'Normal'
            filtros_aplicados.append(f"Tipo: {tipo}")
        if parametros.get('primeira_vez'):
            vez = 'Primeira vez' if parametros['primeira_vez'] == 'true' else 'Recorrentes'
            filtros_aplicados.append(f"Categoria: {vez}")
        if parametros.get('usuario_id'):
            usuario = Usuario.query.get(parametros['usuario_id'])
            if usuario:
                filtros_aplicados.append(f"Usuário: {usuario.nome}")
        if parametros.get('chamadas_apenas') == 'on':
            filtros_aplicados.append("Apenas senhas chamadas")
        
        info_data = {
            'Informação': [
                'Relatório gerado em',
                'Gerado por',
                'Total de registros',
                'Filtros aplicados'
            ],
            'Valor': [
                datetime.now().strftime('%d/%m/%Y às %H:%M:%S'),
                current_user.nome,
                len(senhas),
                ', '.join(filtros_aplicados) if filtros_aplicados else 'Nenhum filtro aplicado'
            ]
        }
        
        info_df = pd.DataFrame(info_data)
        info_df.to_excel(writer, sheet_name='Informações', index=False)
        
        # ============================================================================
        # ABA 3: RESUMO ESTATÍSTICO
        # ============================================================================
        if senhas:
            # Calcular estatísticas
            total_senhas = len(senhas)
            senhas_normais = len([s for s in senhas if s.tipo_paciente == 'normal'])
            senhas_preferenciais = len([s for s in senhas if s.tipo_paciente == 'preferencial'])
            primeira_vez = len([s for s in senhas if s.primeira_vez])
            recorrentes = len([s for s in senhas if not s.primeira_vez])
            senhas_chamadas = len([s for s in senhas if s.chamado])
            senhas_aguardando = len([s for s in senhas if not s.chamado])
            
            stats_data = {
                'Categoria': [
                    'Total de Senhas',
                    'Senhas Normais',
                    'Senhas Preferenciais',
                    'Primeira Vez',
                    'Recorrentes',
                    'Chamadas',
                    'Aguardando'
                ],
                'Quantidade': [
                    total_senhas,
                    senhas_normais,
                    senhas_preferenciais,
                    primeira_vez,
                    recorrentes,
                    senhas_chamadas,
                    senhas_aguardando
                ],
                'Percentual': [
                    '100%',
                    f"{senhas_normais/total_senhas*100:.1f}%" if total_senhas > 0 else '0%',
                    f"{senhas_preferenciais/total_senhas*100:.1f}%" if total_senhas > 0 else '0%',
                    f"{primeira_vez/total_senhas*100:.1f}%" if total_senhas > 0 else '0%',
                    f"{recorrentes/total_senhas*100:.1f}%" if total_senhas > 0 else '0%',
                    f"{senhas_chamadas/total_senhas*100:.1f}%" if total_senhas > 0 else '0%',
                    f"{senhas_aguardando/total_senhas*100:.1f}%" if total_senhas > 0 else '0%'
                ]
            }
            
            stats_df = pd.DataFrame(stats_data)
            stats_df.to_excel(writer, sheet_name='Resumo Estatístico', index=False)
            
            # ============================================================================
            # ABA 4: CHAMADAS POR USUÁRIO
            # ============================================================================
            # Calcular chamadas por usuário
            chamadas_por_usuario = defaultdict(int)
            for senha in senhas:
                if senha.chamado and senha.usuario_chamador:
                    chamadas_por_usuario[senha.usuario_chamador.nome] += 1
            
            if chamadas_por_usuario:
                user_data = []
                for usuario, total in sorted(chamadas_por_usuario.items(), key=lambda x: x[1], reverse=True):
                    percentual = f"{total/senhas_chamadas*100:.1f}%" if senhas_chamadas > 0 else '0%'
                    user_data.append({
                        'Usuário': usuario,
                        'Total de Chamadas': total,
                        'Percentual': percentual
                    })
                
                user_df = pd.DataFrame(user_data)
                user_df.to_excel(writer, sheet_name='Chamadas por Usuário', index=False)
            
            # ============================================================================
            # ABA 5: ANÁLISE TEMPORAL
            # ============================================================================
            # Agrupar por data
            senhas_por_data = defaultdict(int)
            for senha in senhas:
                data = senha.gerado_em.strftime('%d/%m/%Y')
                senhas_por_data[data] += 1
            
            if senhas_por_data:
                temporal_data = []
                for data, total in sorted(senhas_por_data.items()):
                    temporal_data.append({
                        'Data': data,
                        'Total de Senhas': total
                    })
                
                temporal_df = pd.DataFrame(temporal_data)
                temporal_df.to_excel(writer, sheet_name='Análise Temporal', index=False)
    
    buffer.seek(0)
    
    # Retornar arquivo
    from flask import send_file
    return send_file(
        buffer,
        as_attachment=True,
        download_name=f'relatorio_senhas_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx',
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

@bp.route('/api/buscar_usuarios')
@login_required
@role_required('admin')
def buscar_usuarios():
    termo = request.args.get('q', '').strip().lower()
    tipo = request.args.get('tipo', '').strip()
    query = Usuario.query
    if termo:
        query = query.filter(
            (Usuario.nome.ilike(f'%{termo}%')) |
            (Usuario.email.ilike(f'%{termo}%'))
        )
    if tipo:
        query = query.filter(Usuario.tipo == tipo)
    usuarios = query.order_by(Usuario.id).all()
    return jsonify([
        {
            'id': u.id,
            'nome': u.nome,
            'email': u.email,
            'tipo': u.tipo.value if hasattr(u.tipo, 'value') else u.tipo,
        }
        for u in usuarios
    ])
