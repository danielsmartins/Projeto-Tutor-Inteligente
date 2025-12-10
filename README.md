# 🎓 Sistema Tutor Inteligente (STI) para Redação

Este projeto consiste em um **Sistema Tutor Inteligente** focado no auxílio à escrita de redações no modelo ENEM. Diferente de chatbots genéricos, este sistema utiliza uma **Máquina de Estados Finitos (FSM)** para guiar o aluno passo a passo (Introdução, Desenvolvimentos e Conclusão), garantindo que critérios pedagógicos sejam atendidos antes de avançar.

O sistema atua como um mediador entre o aluno e o modelo de linguagem **Google Gemini**, utilizando engenharia de prompt dinâmica para assumir personas de "Professor" (no planejamento) e "Corretor Rigoroso" (na revisão).

---

## 🚀 Funcionalidades

- **Ciclo de Escrita Guiada:** O aluno não escreve o texto todo de uma vez; ele é guiado parágrafo por parágrafo.
- **Validação de Repertório:** Na fase de planejamento, a IA verifica se o repertório sociocultural é pertinente ao tema.
- **Feedback Imediato:** O sistema analisa a coesão e coerência de cada trecho e impede o avanço caso o texto esteja insuficiente (Loop de revisão).
- **Interface Interativa:** Chat amigável desenvolvido com Gradio.
- **Arquitetura Modular:** Código organizado em camadas de responsabilidade (UI, Lógica, Configuração).

---

## 🛠️ Tecnologias Utilizadas

- **Linguagem:** Python 3
- **Interface:** [Gradio](https://www.gradio.app/)
- **IA Generativa:** [Google Gemini API](https://ai.google.dev/) (Modelos Flash 1.5/2.5)
- **Design Pattern:** Máquina de Estados (State Machine) e MVC simplificado.

---

## 📂 Estrutura do Projeto

O código foi refatorado para garantir manutenibilidade e escalabilidade:

```text
projeto-ia/
│
├── main.py           # Ponto de entrada. Execute este arquivo para iniciar.
├── config.py         # Configuração da API Key e inicialização do modelo Gemini.
├── logic.py          # "Cérebro" do sistema: Máquina de estados e validação de regras.
├── ui.py             # Construção da interface visual (Chatbot Gradio).
├── constants.py      # Textos estáticos, prompts base e dicionários de rotinas.
└── requirements.txt  # Lista de dependências do projeto.
