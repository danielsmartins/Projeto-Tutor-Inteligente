
import gradio as gr
from logic import responder_chat, resetar_sessao

def create_ui():
    with gr.Blocks(title="STI Redação") as demo:
        # Estado inicial
        state = gr.State({
            "fase": "config_rotina",
            "rotina_escolhida": [],
            "tema": "",
            "passo_index": 0,
            "texto_acumulado": []
        })

        gr.Markdown("# 🎓 Tutor Inteligente de Redação")

        # Configuração do Chatbot 
        chatbot = gr.Chatbot(
            label="Tutor Virtual",
            height=550,
            value=[{"role": "assistant", "content": "👋 Olá! Sou seu Tutor.\n\nComo quer treinar?\n- **Redação Completa**\n- **Apenas Introdução**\n- **Apenas Desenvolvimento**\n- **Apenas Conclusão**"}]
        )

        with gr.Row():
            msg_input = gr.Textbox(
                scale=4,
                show_label=False,
                placeholder="Digite sua resposta aqui...",
                container=False
            )
            btn_enviar = gr.Button("Enviar", variant="primary", scale=1)
            btn_reiniciar = gr.Button("🔄 Reiniciar", variant="secondary", scale=1)

        # Função wrapper para o botão de reinício
        def acao_botao_reiniciar():
            hist, est = resetar_sessao()
            return hist, est

        # Gatilhos
        msg_input.submit(responder_chat, [msg_input, chatbot, state], [msg_input, chatbot, state])
        btn_enviar.click(responder_chat, [msg_input, chatbot, state], [msg_input, chatbot, state])
        btn_reiniciar.click(acao_botao_reiniciar, outputs=[chatbot, state])

    return demo