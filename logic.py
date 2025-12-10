
from config import model
from constants import ROTINAS, PASSO_INFO

def gerar_tema_aleatorio(eixo=None):
    """Gera um tema se o aluno estiver sem ideias."""
    if not model:
        return "Erro: Modelo não carregado."

    prompt = "Crie um título de tema de redação estilo ENEM, sério e atual. Responda APENAS o título."
    if eixo: prompt += f" O tema deve ser focado no eixo: {eixo}."
    try:
        return model.generate_content(prompt).text.strip()
    except Exception as e:
        print(f"⚠️ Erro ao gerar tema: {e}")
        # Fallback inteligente
        if eixo:
            return f"Tema Livre sobre {eixo.capitalize()} (Erro na IA, defina você o recorte)"
        return "Desafios da educação no Brasil (Tema padrão por erro de conexão)"

def construir_prompt_avaliacao(passo_atual, tema, texto_usuario, historico, ultima_msg_bot=""):
    """Define se a IA deve validar um repertório (planejamento) ou corrigir um texto."""
    contexto = "\n".join(historico)

    if "repertorio" in passo_atual:
        # Prompt de validação de ideia
        instrucao = f"""
        Você é um professor de redação avaliando o PLANEJAMENTO do aluno.
        Tema: '{tema}'.

        CONTEXTO IMEDIATO DO CHAT (Sua última fala): "{ultima_msg_bot}"
        INPUT DO ALUNO: "{texto_usuario}"

        SEU OBJETIVO:
        1. Se o aluno CONCORDAR com sua sugestão anterior (ex: "sim", "pode ser", "gostei", "vamos usar esse", "ok", "vamos com esse"):
           - Inicie com 'TAG: [APROVADO]'.
           - Diga: "Ótima escolha! Esse repertório vai enriquecer muito seu argumento. Vamos em frente."

        2. Se o aluno disser que NÃO SABE, NÃO TEM IDEIA ou PEDIR SUGESTÃO:
           - Inicie com 'TAG: [SUGESTAO]'.
           - Sugira UM repertório sociocultural pertinente (filme, livro, filósofo ou dado estatístico) que se encaixe bem nesse tema.
           - Explique brevemente a conexão.
           - Pergunte: "O que acha de usarmos esse?"

        3. Se o aluno sugeriu um repertório específico (novo):
           - Se a conexão for válida, inicie a resposta com 'TAG: [APROVADO]'. Explique brevemente como conectar ao tema.
           - Se for fraco ou desconexo, inicie com 'TAG: [REVISAR]' e sugira um repertório melhor.
        """
    else:
        # Prompt de correção de texto
        instrucao = f"""
        Você é um corretor rigoroso do ENEM.
        Etapa atual: '{PASSO_INFO[passo_atual]['label']}'.
        Tema: '{tema}'.
        Histórico anterior (partes já aprovadas): {contexto}
        CONTEXTO CHAT: "{ultima_msg_bot}"

        Texto/Input atual do aluno:
        "{texto_usuario}"

        SEU OBJETIVO:
        Analise a intenção do aluno ou o texto enviado.

        1. CASO O ALUNO DIGA QUE VAI REESCREVER (ex: "vou reescrever", "quero tentar de novo", "arrumar"):
           - Responda estritamente com 'TAG: [AGUARDANDO]'.
           - Diga apenas algo como: "Certo, estou no aguardo da sua nova versão." (Não dê a resposta).

        2. CASO O ALUNO PEÇA A RESPOSTA (ex: "mostre como fica", "faça você", "me dê um exemplo", "reescreva para mim"):
           - Responda estritamente com 'TAG: [AVANCAR_COM_MODELO]'.
           - Escreva APENAS o parágrafo corrigido/exemplar completo. NÃO coloque comentários antes ou depois. O que você escrever será salvo automaticamente como o texto do aluno para esta etapa.

        3. CASO SEJA UM TEXTO (tentativa de redação):
           - Se estiver BOM: Inicie com 'TAG: [APROVADO]' e elogie.
           - Se tiver ERROS:
             - Inicie com 'TAG: [REVISAR]'.
             - Cite os trechos ruins entre aspas.
             - Explique o erro.
             - Ao final, PERGUNTE: "Você prefere tentar reescrever com base nessas dicas ou quer que eu gere a versão final para avançarmos?"
        """
    return instrucao

def resetar_sessao():
    """Retorna os valores padrão para reiniciar tudo."""
    novo_estado = {
        "fase": "config_rotina",
        "rotina_escolhida": [],
        "tema": "",
        "passo_index": 0,
        "texto_acumulado": []
    }
    # Mensagem inicial do bot
    novo_historico = [{"role": "assistant", "content": "👋 Olá! Sou seu Tutor.\n\nComo quer treinar?\n- **Redação Completa**\n- **Apenas Introdução**\n- **Apenas Desenvolvimento**\n- **Apenas Conclusão**"}]
    return novo_historico, novo_estado

def responder_chat(mensagem_usuario, historico_visual, estado):
    """Controlador principal da conversa com VALIDAÇÃO RIGOROSA."""

    # 0. Verifica comando de reinício via texto
    if mensagem_usuario.strip().lower() in ["reiniciar", "reset", "começar de novo", "limpar"]:
        hist, est = resetar_sessao()
        return "", hist, est

    # Inicializa o histórico se estiver vazio
    if historico_visual is None: historico_visual = []

    # Recupera a última mensagem do assistente para contexto
    ultima_msg_bot = ""
    for msg in reversed(historico_visual):
        if msg["role"] == "assistant":
            ultima_msg_bot = msg["content"]
            break

    # Adiciona mensagem do usuário ao chat visual
    historico_visual.append({"role": "user", "content": mensagem_usuario})

    msg_bot = ""
    msg_usuario_lower = mensagem_usuario.strip().lower()

    # --- MAQUINA DE ESTADOS ---

    # Escolha da Rotina
    if estado["fase"] == "config_rotina":
        chave = None

        # Validação explícita
        if any(k in msg_usuario_lower for k in ["completa", "tudo", "todas"]):
            chave = "Completa"
        elif any(k in msg_usuario_lower for k in ["intro", "início", "começo"]):
            chave = "Apenas Introdução"
        elif any(k in msg_usuario_lower for k in ["desen", "meio"]):
            chave = "Apenas Desenvolvimento"
        elif any(k in msg_usuario_lower for k in ["concl", "fim", "final"]):
            chave = "Apenas Conclusão"

        # Se não entendeu, rejeita e pede novamente
        if chave is None:
            msg_bot = "⚠️ **Opção inválida.**\nPor favor, escolha uma das opções:\n- **Redação Completa**\n- **Apenas Introdução**\n- **Apenas Desenvolvimento**\n- **Apenas Conclusão**"
        else:
            estado["rotina_escolhida"] = ROTINAS[chave]
            estado["fase"] = "config_tema"
            msg_bot = f"🛠️ **Modo:** {chave}\n\nAgora o **TEMA**:\n1. Digite um tema específico;\n2. Digite um Eixo (ex: Saúde, Tecnologia);\n3. Digite 'Aleatório'."

    # Escolha do Tema
    elif estado["fase"] == "config_tema":
        entrada = msg_usuario_lower
        aviso = ""
        tema_valido = False
        tema_final = ""

        # Lista de gatilhos para pedir ajuda/tema aleatório
        gatilhos_ajuda = [
            "aleat", "random", "sorte", "gera",
            "não sei", "nao sei", "sem ideia", "sem idéia",
            "qualquer um", "sugira", "indique", "escolha", "me dê um"
        ]
        
        # Lista de Eixos Comuns 
        eixos_comuns = ["saude", "saúde", "tecno", "ciência", "educa", "ensino", "ambien", "natureza", "social", "socieda", "cultura", "arte", "seguran"]

        # Lista negra (coisas que parecem conversa)
        blacklist = ["não", "nao", "sim", "ok", "talvez", "oi", "olá", "teste", "quero", "pode ser"]

        # 1. Checa se o usuário pediu ajuda (Aleatório)
        if any(x in entrada for x in gatilhos_ajuda):
            tema_final = gerar_tema_aleatorio()
            aviso = "🎲 Você pediu ajuda, então sorteei um tema para você!"
            tema_valido = True

        # 2. VERIFICAÇÃO DE EIXO (PRIORIDADE ALTA - Agora vem antes da validação de tamanho)
        elif any(eixo in entrada for eixo in eixos_comuns):
             tema_final = gerar_tema_aleatorio(eixo=entrada)
             aviso = f"🎯 Entendi que você quer falar sobre '{entrada}'. Gere um tema focado nisso!"
             tema_valido = True

        # 3. Validação de Tamanho e Blacklist (Só roda se não for ajuda nem eixo)
        elif len(entrada) < 10 or entrada in blacklist:
            msg_bot = "⚠️ **Isso não parece um tema válido.**\nO tema precisa ser um título descritivo. \n\nExemplos:\n- *Insegurança alimentar no Brasil*\n- *O estigma das doenças mentais*\n\n👉 Se estiver sem ideias, digite **'Não sei'**, **'Aleatório'** ou um eixo como **'Saúde'**."
            historico_visual.append({"role": "assistant", "content": msg_bot})
            return "", historico_visual, estado

        # 4. Validação Semântica (Para títulos específicos digitados pelo usuário)
        else:
            # Validação Semântica Rápida com IA
            try:
                check_prompt = f"A frase '{mensagem_usuario}' é um título válido para um tema de redação do ENEM ou similar? Responda APENAS 'SIM' ou 'NAO'."
                check_resp = model.generate_content(check_prompt).text.strip().upper()
                if "NAO" in check_resp:
                    msg_bot = f"⚠️ **A IA analisou e acha que '{mensagem_usuario}' não é um bom tema de redação.**\n\nTente ser mais formal ou digite **'Aleatório'**."
                    historico_visual.append({"role": "assistant", "content": msg_bot})
                    return "", historico_visual, estado
            except:
                pass # Se der erro na verificação, aceita o tema para não travar

            tema_final = mensagem_usuario
            aviso = "✍️ Tema registrado."
            tema_valido = True

        # Só avança se passou por todas as barreiras
        if tema_valido:
            estado["tema"] = tema_final
            estado["fase"] = "escrita"
            estado["passo_index"] = 0

            p = estado["rotina_escolhida"][0]
            info = PASSO_INFO[p]
            msg_bot = f"{aviso}\n\n📌 **TEMA:** {tema_final}\n\n---\nVamos começar!\n👉 **{info['label']}**\n{info['desc']}"

    # Escrita e Feedback
    elif estado["fase"] == "escrita":
        passos = estado["rotina_escolhida"]
        idx = estado["passo_index"]
        p_atual = passos[idx]

        # Validação básica de input
        if len(mensagem_usuario.strip()) < 3:
             msg_bot = "⚠️ **Resposta muito curta.**\nPor favor, desenvolva mais sua resposta ou digite 'Pular' se a etapa permitir."
             historico_visual.append({"role": "assistant", "content": msg_bot})
             return "", historico_visual, estado

        # Logica de comando pular
        if msg_usuario_lower in ["pular", "skip", "proximo", "próximo"]:
            if "d2" in p_atual and "conclusao" in passos:
                idx_concl = passos.index("conclusao")
                estado["passo_index"] = idx_concl
                estado["texto_acumulado"].append("\n[Desenvolvimento 2 não realizado por opção do aluno]\n")
                info = PASSO_INFO["conclusao"]
                msg_bot = f"⏩ **Entendido, vamos pular o Desenvolvimento 2.**\n\nAgora, foque no gran finale:\n👉 **{info['label']}**\n{info['desc']}"
                historico_visual.append({"role": "assistant", "content": msg_bot})
                return "", historico_visual, estado
            else:
                 msg_bot = "⚠️ **Não é possível pular esta etapa.** É essencial para a estrutura da redação."
                 historico_visual.append({"role": "assistant", "content": msg_bot})
                 return "", historico_visual, estado

        # Chama o Gemini
        prompt = construir_prompt_avaliacao(p_atual, estado["tema"], mensagem_usuario, estado["texto_acumulado"], ultima_msg_bot)

        try:
            resp_ia = model.generate_content(prompt).text
        except Exception as e:
            print(f"Erro na avaliação: {e}")
            resp_ia = "TAG: [REVISAR] Erro de conexão com a IA. Por favor, tente enviar sua resposta novamente."

        # Logica de respostas tags
        if "TAG: [APROVADO]" in resp_ia:
            feedback = resp_ia.replace("TAG: [APROVADO]", "✅ **Muito bem!**")
            if "repertorio" not in p_atual:
                estado["texto_acumulado"].append(mensagem_usuario)
            estado["passo_index"] += 1

            if estado["passo_index"] >= len(passos):
                final = "\n\n".join(estado["texto_acumulado"])
                msg_bot = f"{feedback}\n\n🏆 **Sessão Concluída!** Texto final:\n\n{final}"
                estado["fase"] = "fim"
            else:
                prox = passos[estado["passo_index"]]
                info = PASSO_INFO[prox]
                msg_bot = f"{feedback}\n\n👉 **Próximo:** {info['label']}\n{info['desc']}"

        elif "TAG: [AVANCAR_COM_MODELO]" in resp_ia:
            texto_modelo = resp_ia.replace("TAG: [AVANCAR_COM_MODELO]", "").strip()
            if "repertorio" not in p_atual:
                estado["texto_acumulado"].append(texto_modelo)
            estado["passo_index"] += 1

            if estado["passo_index"] >= len(passos):
                final = "\n\n".join(estado["texto_acumulado"])
                msg_bot = f"✅ **Versão Gerada e Salva:**\n\n> *{texto_modelo}*\n\n🏆 **Sessão Concluída!** Texto final:\n\n{final}"
                estado["fase"] = "fim"
            else:
                prox = passos[estado["passo_index"]]
                info = PASSO_INFO[prox]
                msg_bot = f"✅ **Versão Gerada e Aceita:**\n\n> *{texto_modelo}*\n\n---\n👉 **Próximo:** {info['label']}\n{info['desc']}"

        elif "TAG: [AGUARDANDO]" in resp_ia:
            msg_bot = resp_ia.replace("TAG: [AGUARDANDO]", "⏳")

        elif "TAG: [SUGESTAO]" in resp_ia:
            msg_bot = resp_ia.replace("TAG: [SUGESTAO]", "💡 **Sugestão do Tutor:**")

        else:
            msg_bot = resp_ia.replace("TAG: [REVISAR]", "⚠️ **Atenção:**")

    elif estado["fase"] == "fim":
        msg_bot = "A sessão acabou. Clique em 'Reiniciar' ou digite 'reiniciar' para começar de novo."

    # Adiciona resposta do Bot e retorna
    historico_visual.append({"role": "assistant", "content": msg_bot})
    return "", historico_visual, estado