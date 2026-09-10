import streamlit as st
from groq import Groq
from datetime import datetime
import json

st.set_page_config(page_title="Ghost Writer IA", page_icon="✍️", layout="wide")

st.markdown("""
    <style>

    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    .stApp { background-color:#F0FDFA; font-family:'Inter',sans-serif; }
    [data-testid="stSidebar"] { display:none; }
    .stTextInput>div>div>input, .stTextArea>div>textarea,
    .stSelectbox>div>div>div, .stNumberInput>div>div>input {
        background-color:#FFFFFF !important; color:#1A1A2E !important;
        border:1px solid #CED4DA !important; font-family:'Inter',sans-serif !important;
    }
    .stButton>button {
        width:100%; border-radius:10px; height:3.2em;
        background:linear-gradient(135deg,#0F766E,#0D9488) !important; color:white !important;
        font-weight:600; border:none; box-shadow:2px 2px 8px rgba(0,0,0,0.1);
        font-family:'Inter',sans-serif !important; transition:all 0.2s ease;
    }
    .stButton>button:hover { background:linear-gradient(135deg,#0D9488,#0F766E) !important; transform:translateY(-1px); }
    .stApp .stButton>button, .stApp .stButton>button p,
    .stApp .stButton>button span, .stApp .stButton>button div { color:white !important; }
    .stApp h1, .stApp h2, .stApp h3 { color:#134E4A !important; font-family:'Inter',sans-serif !important; font-weight:700 !important; }
    .card { background:linear-gradient(135deg,#F0FDFA,#CCFBF1); padding:20px; border-radius:14px; border:1px solid #5EEAD4; margin-bottom:14px; white-space:normal; word-wrap:break-word; }
    .stApp .card, .stApp .card p, .stApp .card span, .stApp .card div, .stApp .card strong { color:#134E4A !important; }
    .card-blue { background:linear-gradient(135deg,#EFF6FF,#DBEAFE); padding:20px; border-radius:14px; border:1px solid #93C5FD; margin-bottom:14px; }
    .stApp .card-blue, .stApp .card-blue p, .stApp .card-blue div { color:#1E3A8A !important; }
    .card-red { background:linear-gradient(135deg,#FFF5F5,#FEE2E2); padding:20px; border-radius:14px; border:1px solid #FECACA; margin-bottom:14px; }
    .stApp .card-red, .stApp .card-red p, .stApp .card-red div { color:#7F1D1D !important; }
    .card-green { background:linear-gradient(135deg,#F0FDF4,#DCFCE7); padding:20px; border-radius:14px; border:1px solid #86EFAC; margin-bottom:14px; }
    .stApp .card-green, .stApp .card-green p, .stApp .card-green div { color:#14532D !important; }
    .card-yellow { background:linear-gradient(135deg,#FFFBEB,#FEF3C7); padding:18px; border-radius:12px; border:1px solid #FCD34D; margin-bottom:12px; }
    .stApp .card-yellow, .stApp .card-yellow p, .stApp .card-yellow div { color:#78350F !important; }
    .badge { background:#0F766E; color:white !important; padding:4px 12px; border-radius:20px; font-size:0.78em; font-weight:600; display:inline-block; margin:2px; }
    .badge-verde { background:#059669; color:white !important; padding:4px 12px; border-radius:20px; font-size:0.78em; font-weight:600; display:inline-block; margin:2px; }
    .badge-amarelo { background:#B45309; color:white !important; padding:4px 12px; border-radius:20px; font-size:0.78em; font-weight:600; display:inline-block; margin:2px; }
    .badge-roxo { background:#6D28D9; color:white !important; padding:4px 12px; border-radius:20px; font-size:0.78em; font-weight:600; display:inline-block; margin:2px; }
    .divider { border:none; height:1px; background:linear-gradient(to right,transparent,#5EEAD4,transparent); margin:18px 0; }
    .hist-item { background:#FFFFFF; border-radius:10px; padding:12px 16px; margin-bottom:8px; border-left:4px solid #5EEAD4; }
    .stApp .hist-item, .stApp .hist-item p, .stApp .hist-item span, .stApp .hist-item div { color:#134E4A !important; }
    .stat-box { background:#FFFFFF; border-radius:12px; padding:16px; text-align:center; border:1px solid #5EEAD4; }
    .stApp .stat-box div, .stApp .stat-box span { color:#134E4A !important; }
    .chat-user { background:#FFFFFF; border:1px solid #5EEAD4; border-radius:12px 12px 4px 12px; padding:12px 16px; margin:8px 0; }
    .stApp .chat-user, .stApp .chat-user p, .stApp .chat-user div { color:#134E4A !important; }
    .chat-persona { background:#CCFBF1; border:1px solid #5EEAD4; border-radius:4px 12px 12px 12px; padding:12px 16px; margin:8px 0; }
    .stApp .chat-persona, .stApp .chat-persona p, .stApp .chat-persona div { color:#134E4A !important; }

    </style>
""", unsafe_allow_html=True)

SYSTEM_PROMPT = "Você é um ghostwriter especialista em criação de conteúdo autêntico. Aprende o estilo, tom e voz do usuário e escreve como se fosse ele — nunca como IA. Cria posts, artigos, e-mails, e-books e roteiros que soam genuinamente humanos. Português do Brasil."

@st.cache_resource
def get_cache_ghost_writer():
    return {"perfis": {}}

_cache = get_cache_ghost_writer()

CHAVES_SALVAR = ["usuario","historico_ghost_writer"]

def gerar_json():
    return json.dumps({k: st.session_state.get(k) for k in CHAVES_SALVAR}, ensure_ascii=False, indent=2, default=str)

def carregar_json_sessao(dados):
    for k,v in dados.items():
        if k in CHAVES_SALVAR:
            st.session_state[k] = v

def salvar_perfil_cache(usuario):
    _cache["perfis"][usuario] = {k: st.session_state.get(k) for k in CHAVES_SALVAR}

def perfis_salvos():
    return [p for p in _cache["perfis"].keys() if len(p.strip()) >= 2]

def carregar_perfil_cache(usuario):
    return _cache["perfis"].get(usuario)

defaults = {
    "etapa": "Login", "usuario": "", "api_key": "",
    "historico_ghost_writer": [],
}
for k,v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ── LOGIN ──
if st.session_state.etapa == "Login":
    st.markdown("# ✍️ Ghost Writer IA")
    st.markdown("<div class=\'card\'><b>🔒 ACESSO RESTRITO A CLIENTES DO QUIZ COM PRÊMIOS</b><br>🔗 quizcompremios.com.br</div>", unsafe_allow_html=True)
    st.info("💻 **Dica:** Pela complexidade dos agentes, no computador a experiência é mais agradável.")
    with st.container():
        nome  = st.text_input("Seu Nome:", key="nome_login")
        chave = st.text_input("🔑 Sua Chave API da Groq:", type="password", key="chave_login")
        arq_j = st.file_uploader("📂 Carregar dados salvos (.json):", type=["json"], key="upload_login")
        dados_login = json.load(arq_j) if arq_j else None
        if st.button("✨ ENTRAR", key="btn_entrar_login"):
            if len(nome.strip()) < 2:
                st.warning("Digite um nome com pelo menos 2 caracteres.")
            elif chave.strip():
                st.session_state.usuario = nome.strip()
                st.session_state.api_key = chave
                if dados_login: carregar_json_sessao(dados_login)
                st.session_state.etapa = "App"
                st.rerun()
            else:
                st.warning("Preencha nome e chave API.")

elif st.session_state.etapa == "App":
    historico = st.session_state.get("historico_ghost_writer", [])
    salvar_perfil_cache(st.session_state.usuario)

    _tab_home_gw, _tab_estilo_gw, _tab_posts_redes, _tab_artigos, _tab_emails_gw, _tab_ebook_gw, _tab_roteiros, _tab_threads, _tab_legendas, _tab_ideias_gw, _tab_calendario_gw, _tab_salvos_gw = st.tabs(['🏠 Home', '🎙️ Minha Voz e Estilo', '📱 Posts para Redes', '📝 Artigos e Blog', '📧 E-mails', '📚 E-book', '🎬 Roteiros de Vídeo', '🧵 Threads', '📣 Legendas', '💡 Ideias de Conteúdo', '📅 Calendário Editorial', '📂 Meus Textos'])

    with _tab_home_gw:
        st.title(f"✍️ Olá, {st.session_state.usuario}!")
        st.markdown(f"*Sua voz, amplificada pela IA — conteúdo que soa como você.*")
        st.markdown("<hr class='divider'>", unsafe_allow_html=True)
        st.markdown(f"### Bem-vindo ao **Ghost Writer IA**")
        st.markdown(f"<div class='card'>Use as abas acima para navegar entre as funcionalidades. Cada aba oferece uma ferramenta diferente com IA.</div>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        with col1: st.markdown(f"<div class='stat-box'><div style='font-size:1.8em;'>🏠</div><div style='font-size:0.8em;'>Ghost Writer IA</div></div>", unsafe_allow_html=True)
        with col2: st.markdown(f"<div class='stat-box'><div style='font-size:1.8em;'>🤖</div><div style='font-size:0.8em;'>Powered by IA</div></div>", unsafe_allow_html=True)
        with col3: st.markdown(f"<div class='stat-box'><div style='font-size:1.8em;'>💾</div><div style='font-size:0.8em;'>Salve seus dados</div></div>", unsafe_allow_html=True)
        st.markdown("<hr class='divider'>", unsafe_allow_html=True)
        col_sv, _ = st.columns([1,3])
        with col_sv:
            st.download_button("💾 Salvar dados (.json)", data=json.dumps({k:st.session_state.get(k) for k in CHAVES_SALVAR}, ensure_ascii=False, indent=2, default=str), file_name=f"ghost_writer_{st.session_state.usuario}.json", mime="application/json", key="dl_ghost__1")

    with _tab_estilo_gw:
        st.header("🎙️ Minha Voz e Estilo")
        prompt_estilo_gw = st.text_area("Descreva sua situação ou dúvida:", height=120, key="prompt_estilo_gw", placeholder="Digite aqui...")
        if st.button("🤖 GERAR COM IA", key="btn_estilo_gw", use_container_width=True):
            if prompt_estilo_gw.strip():
                with st.spinner("A IA está analisando..."):
                    try:
                        client = Groq(api_key=st.session_state.api_key)
                        msgs = [{"role":"system","content":SYSTEM_PROMPT},{"role":"user","content":prompt_estilo_gw}]
                        resp = client.chat.completions.create(messages=msgs, model="openai/gpt-oss-120b", max_tokens=2048)
                        resultado_estilo_gw = resp.choices[0].message.content
                        st.session_state["res_estilo_gw"] = resultado_estilo_gw
                        historico.append({"data":datetime.now().strftime("%d/%m %H:%M"),"aba":"Minha Voz e Estilo","resumo":prompt_estilo_gw[:60],"conteudo":resultado_estilo_gw})
                        st.session_state.historico_ghost_writer = historico
                    except Exception as e:
                        st.error(f"Erro na API: {e}")
            else:
                st.warning("Digite sua situação antes de gerar.")
        if st.session_state.get("res_estilo_gw"):
            st.markdown(f"<div class='card'>{st.session_state['res_estilo_gw']}</div>", unsafe_allow_html=True)
            st.download_button("📋 Baixar resultado", data=st.session_state["res_estilo_gw"], file_name="estilo_gw_resultado.txt", mime="text/plain", key="dl_estilo_gw")

    with _tab_posts_redes:
        st.header("📱 Posts para Redes")
        prompt_posts_redes = st.text_area("Descreva sua situação ou dúvida:", height=120, key="prompt_posts_redes", placeholder="Digite aqui...")
        if st.button("🤖 GERAR COM IA", key="btn_posts_redes", use_container_width=True):
            if prompt_posts_redes.strip():
                with st.spinner("A IA está analisando..."):
                    try:
                        client = Groq(api_key=st.session_state.api_key)
                        msgs = [{"role":"system","content":SYSTEM_PROMPT},{"role":"user","content":prompt_posts_redes}]
                        resp = client.chat.completions.create(messages=msgs, model="openai/gpt-oss-120b", max_tokens=2048)
                        resultado_posts_redes = resp.choices[0].message.content
                        st.session_state["res_posts_redes"] = resultado_posts_redes
                        historico.append({"data":datetime.now().strftime("%d/%m %H:%M"),"aba":"Posts para Redes","resumo":prompt_posts_redes[:60],"conteudo":resultado_posts_redes})
                        st.session_state.historico_ghost_writer = historico
                    except Exception as e:
                        st.error(f"Erro na API: {e}")
            else:
                st.warning("Digite sua situação antes de gerar.")
        if st.session_state.get("res_posts_redes"):
            st.markdown(f"<div class='card'>{st.session_state['res_posts_redes']}</div>", unsafe_allow_html=True)
            st.download_button("📋 Baixar resultado", data=st.session_state["res_posts_redes"], file_name="posts_redes_resultado.txt", mime="text/plain", key="dl_posts_redes")

    with _tab_artigos:
        st.header("📝 Artigos e Blog")
        prompt_artigos = st.text_area("Descreva sua situação ou dúvida:", height=120, key="prompt_artigos", placeholder="Digite aqui...")
        if st.button("🤖 GERAR COM IA", key="btn_artigos", use_container_width=True):
            if prompt_artigos.strip():
                with st.spinner("A IA está analisando..."):
                    try:
                        client = Groq(api_key=st.session_state.api_key)
                        msgs = [{"role":"system","content":SYSTEM_PROMPT},{"role":"user","content":prompt_artigos}]
                        resp = client.chat.completions.create(messages=msgs, model="openai/gpt-oss-120b", max_tokens=2048)
                        resultado_artigos = resp.choices[0].message.content
                        st.session_state["res_artigos"] = resultado_artigos
                        historico.append({"data":datetime.now().strftime("%d/%m %H:%M"),"aba":"Artigos e Blog","resumo":prompt_artigos[:60],"conteudo":resultado_artigos})
                        st.session_state.historico_ghost_writer = historico
                    except Exception as e:
                        st.error(f"Erro na API: {e}")
            else:
                st.warning("Digite sua situação antes de gerar.")
        if st.session_state.get("res_artigos"):
            st.markdown(f"<div class='card'>{st.session_state['res_artigos']}</div>", unsafe_allow_html=True)
            st.download_button("📋 Baixar resultado", data=st.session_state["res_artigos"], file_name="artigos_resultado.txt", mime="text/plain", key="dl_artigos")

    with _tab_emails_gw:
        st.header("📧 E-mails")
        prompt_emails_gw = st.text_area("Descreva sua situação ou dúvida:", height=120, key="prompt_emails_gw", placeholder="Digite aqui...")
        if st.button("🤖 GERAR COM IA", key="btn_emails_gw", use_container_width=True):
            if prompt_emails_gw.strip():
                with st.spinner("A IA está analisando..."):
                    try:
                        client = Groq(api_key=st.session_state.api_key)
                        msgs = [{"role":"system","content":SYSTEM_PROMPT},{"role":"user","content":prompt_emails_gw}]
                        resp = client.chat.completions.create(messages=msgs, model="openai/gpt-oss-120b", max_tokens=2048)
                        resultado_emails_gw = resp.choices[0].message.content
                        st.session_state["res_emails_gw"] = resultado_emails_gw
                        historico.append({"data":datetime.now().strftime("%d/%m %H:%M"),"aba":"E-mails","resumo":prompt_emails_gw[:60],"conteudo":resultado_emails_gw})
                        st.session_state.historico_ghost_writer = historico
                    except Exception as e:
                        st.error(f"Erro na API: {e}")
            else:
                st.warning("Digite sua situação antes de gerar.")
        if st.session_state.get("res_emails_gw"):
            st.markdown(f"<div class='card'>{st.session_state['res_emails_gw']}</div>", unsafe_allow_html=True)
            st.download_button("📋 Baixar resultado", data=st.session_state["res_emails_gw"], file_name="emails_gw_resultado.txt", mime="text/plain", key="dl_emails_gw")

    with _tab_ebook_gw:
        st.header("📚 E-book")
        prompt_ebook_gw = st.text_area("Descreva sua situação ou dúvida:", height=120, key="prompt_ebook_gw", placeholder="Digite aqui...")
        if st.button("🤖 GERAR COM IA", key="btn_ebook_gw", use_container_width=True):
            if prompt_ebook_gw.strip():
                with st.spinner("A IA está analisando..."):
                    try:
                        client = Groq(api_key=st.session_state.api_key)
                        msgs = [{"role":"system","content":SYSTEM_PROMPT},{"role":"user","content":prompt_ebook_gw}]
                        resp = client.chat.completions.create(messages=msgs, model="openai/gpt-oss-120b", max_tokens=2048)
                        resultado_ebook_gw = resp.choices[0].message.content
                        st.session_state["res_ebook_gw"] = resultado_ebook_gw
                        historico.append({"data":datetime.now().strftime("%d/%m %H:%M"),"aba":"E-book","resumo":prompt_ebook_gw[:60],"conteudo":resultado_ebook_gw})
                        st.session_state.historico_ghost_writer = historico
                    except Exception as e:
                        st.error(f"Erro na API: {e}")
            else:
                st.warning("Digite sua situação antes de gerar.")
        if st.session_state.get("res_ebook_gw"):
            st.markdown(f"<div class='card'>{st.session_state['res_ebook_gw']}</div>", unsafe_allow_html=True)
            st.download_button("📋 Baixar resultado", data=st.session_state["res_ebook_gw"], file_name="ebook_gw_resultado.txt", mime="text/plain", key="dl_ebook_gw")

    with _tab_roteiros:
        st.header("🎬 Roteiros de Vídeo")
        prompt_roteiros = st.text_area("Descreva sua situação ou dúvida:", height=120, key="prompt_roteiros", placeholder="Digite aqui...")
        if st.button("🤖 GERAR COM IA", key="btn_roteiros", use_container_width=True):
            if prompt_roteiros.strip():
                with st.spinner("A IA está analisando..."):
                    try:
                        client = Groq(api_key=st.session_state.api_key)
                        msgs = [{"role":"system","content":SYSTEM_PROMPT},{"role":"user","content":prompt_roteiros}]
                        resp = client.chat.completions.create(messages=msgs, model="openai/gpt-oss-120b", max_tokens=2048)
                        resultado_roteiros = resp.choices[0].message.content
                        st.session_state["res_roteiros"] = resultado_roteiros
                        historico.append({"data":datetime.now().strftime("%d/%m %H:%M"),"aba":"Roteiros de Vídeo","resumo":prompt_roteiros[:60],"conteudo":resultado_roteiros})
                        st.session_state.historico_ghost_writer = historico
                    except Exception as e:
                        st.error(f"Erro na API: {e}")
            else:
                st.warning("Digite sua situação antes de gerar.")
        if st.session_state.get("res_roteiros"):
            st.markdown(f"<div class='card'>{st.session_state['res_roteiros']}</div>", unsafe_allow_html=True)
            st.download_button("📋 Baixar resultado", data=st.session_state["res_roteiros"], file_name="roteiros_resultado.txt", mime="text/plain", key="dl_roteiros")

    with _tab_threads:
        st.header("🧵 Threads")
        prompt_threads = st.text_area("Descreva sua situação ou dúvida:", height=120, key="prompt_threads", placeholder="Digite aqui...")
        if st.button("🤖 GERAR COM IA", key="btn_threads", use_container_width=True):
            if prompt_threads.strip():
                with st.spinner("A IA está analisando..."):
                    try:
                        client = Groq(api_key=st.session_state.api_key)
                        msgs = [{"role":"system","content":SYSTEM_PROMPT},{"role":"user","content":prompt_threads}]
                        resp = client.chat.completions.create(messages=msgs, model="openai/gpt-oss-120b", max_tokens=2048)
                        resultado_threads = resp.choices[0].message.content
                        st.session_state["res_threads"] = resultado_threads
                        historico.append({"data":datetime.now().strftime("%d/%m %H:%M"),"aba":"Threads","resumo":prompt_threads[:60],"conteudo":resultado_threads})
                        st.session_state.historico_ghost_writer = historico
                    except Exception as e:
                        st.error(f"Erro na API: {e}")
            else:
                st.warning("Digite sua situação antes de gerar.")
        if st.session_state.get("res_threads"):
            st.markdown(f"<div class='card'>{st.session_state['res_threads']}</div>", unsafe_allow_html=True)
            st.download_button("📋 Baixar resultado", data=st.session_state["res_threads"], file_name="threads_resultado.txt", mime="text/plain", key="dl_threads")

    with _tab_legendas:
        st.header("📣 Legendas")
        prompt_legendas = st.text_area("Descreva sua situação ou dúvida:", height=120, key="prompt_legendas", placeholder="Digite aqui...")
        if st.button("🤖 GERAR COM IA", key="btn_legendas", use_container_width=True):
            if prompt_legendas.strip():
                with st.spinner("A IA está analisando..."):
                    try:
                        client = Groq(api_key=st.session_state.api_key)
                        msgs = [{"role":"system","content":SYSTEM_PROMPT},{"role":"user","content":prompt_legendas}]
                        resp = client.chat.completions.create(messages=msgs, model="openai/gpt-oss-120b", max_tokens=2048)
                        resultado_legendas = resp.choices[0].message.content
                        st.session_state["res_legendas"] = resultado_legendas
                        historico.append({"data":datetime.now().strftime("%d/%m %H:%M"),"aba":"Legendas","resumo":prompt_legendas[:60],"conteudo":resultado_legendas})
                        st.session_state.historico_ghost_writer = historico
                    except Exception as e:
                        st.error(f"Erro na API: {e}")
            else:
                st.warning("Digite sua situação antes de gerar.")
        if st.session_state.get("res_legendas"):
            st.markdown(f"<div class='card'>{st.session_state['res_legendas']}</div>", unsafe_allow_html=True)
            st.download_button("📋 Baixar resultado", data=st.session_state["res_legendas"], file_name="legendas_resultado.txt", mime="text/plain", key="dl_legendas")

    with _tab_ideias_gw:
        st.header("💡 Ideias de Conteúdo")
        prompt_ideias_gw = st.text_area("Descreva sua situação ou dúvida:", height=120, key="prompt_ideias_gw", placeholder="Digite aqui...")
        if st.button("🤖 GERAR COM IA", key="btn_ideias_gw", use_container_width=True):
            if prompt_ideias_gw.strip():
                with st.spinner("A IA está analisando..."):
                    try:
                        client = Groq(api_key=st.session_state.api_key)
                        msgs = [{"role":"system","content":SYSTEM_PROMPT},{"role":"user","content":prompt_ideias_gw}]
                        resp = client.chat.completions.create(messages=msgs, model="openai/gpt-oss-120b", max_tokens=2048)
                        resultado_ideias_gw = resp.choices[0].message.content
                        st.session_state["res_ideias_gw"] = resultado_ideias_gw
                        historico.append({"data":datetime.now().strftime("%d/%m %H:%M"),"aba":"Ideias de Conteúdo","resumo":prompt_ideias_gw[:60],"conteudo":resultado_ideias_gw})
                        st.session_state.historico_ghost_writer = historico
                    except Exception as e:
                        st.error(f"Erro na API: {e}")
            else:
                st.warning("Digite sua situação antes de gerar.")
        if st.session_state.get("res_ideias_gw"):
            st.markdown(f"<div class='card'>{st.session_state['res_ideias_gw']}</div>", unsafe_allow_html=True)
            st.download_button("📋 Baixar resultado", data=st.session_state["res_ideias_gw"], file_name="ideias_gw_resultado.txt", mime="text/plain", key="dl_ideias_gw")

    with _tab_calendario_gw:
        st.header("📅 Calendário Editorial")
        prompt_calendario_gw = st.text_area("Descreva sua situação ou dúvida:", height=120, key="prompt_calendario_gw", placeholder="Digite aqui...")
        if st.button("🤖 GERAR COM IA", key="btn_calendario_gw", use_container_width=True):
            if prompt_calendario_gw.strip():
                with st.spinner("A IA está analisando..."):
                    try:
                        client = Groq(api_key=st.session_state.api_key)
                        msgs = [{"role":"system","content":SYSTEM_PROMPT},{"role":"user","content":prompt_calendario_gw}]
                        resp = client.chat.completions.create(messages=msgs, model="openai/gpt-oss-120b", max_tokens=2048)
                        resultado_calendario_gw = resp.choices[0].message.content
                        st.session_state["res_calendario_gw"] = resultado_calendario_gw
                        historico.append({"data":datetime.now().strftime("%d/%m %H:%M"),"aba":"Calendário Editorial","resumo":prompt_calendario_gw[:60],"conteudo":resultado_calendario_gw})
                        st.session_state.historico_ghost_writer = historico
                    except Exception as e:
                        st.error(f"Erro na API: {e}")
            else:
                st.warning("Digite sua situação antes de gerar.")
        if st.session_state.get("res_calendario_gw"):
            st.markdown(f"<div class='card'>{st.session_state['res_calendario_gw']}</div>", unsafe_allow_html=True)
            st.download_button("📋 Baixar resultado", data=st.session_state["res_calendario_gw"], file_name="calendario_gw_resultado.txt", mime="text/plain", key="dl_calendario_gw")

    with _tab_salvos_gw:
        st.header("📂 Meus Textos")
        prompt_salvos_gw = st.text_area("Descreva sua situação ou dúvida:", height=120, key="prompt_salvos_gw", placeholder="Digite aqui...")
        if st.button("🤖 GERAR COM IA", key="btn_salvos_gw", use_container_width=True):
            if prompt_salvos_gw.strip():
                with st.spinner("A IA está analisando..."):
                    try:
                        client = Groq(api_key=st.session_state.api_key)
                        msgs = [{"role":"system","content":SYSTEM_PROMPT},{"role":"user","content":prompt_salvos_gw}]
                        resp = client.chat.completions.create(messages=msgs, model="openai/gpt-oss-120b", max_tokens=2048)
                        resultado_salvos_gw = resp.choices[0].message.content
                        st.session_state["res_salvos_gw"] = resultado_salvos_gw
                        historico.append({"data":datetime.now().strftime("%d/%m %H:%M"),"aba":"Meus Textos","resumo":prompt_salvos_gw[:60],"conteudo":resultado_salvos_gw})
                        st.session_state.historico_ghost_writer = historico
                    except Exception as e:
                        st.error(f"Erro na API: {e}")
            else:
                st.warning("Digite sua situação antes de gerar.")
        if st.session_state.get("res_salvos_gw"):
            st.markdown(f"<div class='card'>{st.session_state['res_salvos_gw']}</div>", unsafe_allow_html=True)
            st.download_button("📋 Baixar resultado", data=st.session_state["res_salvos_gw"], file_name="salvos_gw_resultado.txt", mime="text/plain", key="dl_salvos_gw")


# --- RODAPÉ ---
st.markdown("<hr class='divider'>", unsafe_allow_html=True)
st.markdown(f"<div style='text-align:center;font-size:0.75em;color:#94A3B8;'>© 2026 Ghost Writer IA · Quiz Com Prêmios</div>", unsafe_allow_html=True)
