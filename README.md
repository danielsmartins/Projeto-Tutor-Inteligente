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
```
## ⚙️ Instalação e Configuração
Siga os passos abaixo para rodar o projeto localmente.

1. Pré-requisitos
Certifique-se de ter o Python instalado em sua máquina.

2. Clonar ou Baixar
Baixe os arquivos do projeto para uma pasta em seu computador.

3. Instalar Dependências
Abra o terminal na pasta do projeto e execute:

```Bash

pip install -r requirements.txt
```
## 🔑 Configurando a API Key (Importante)
Para que a inteligência artificial funcione, você precisa de uma chave de API do Google Gemini.

Gere sua chave gratuitamente no Google AI Studio.

Abra o arquivo config.py no seu editor de código.

Localize a variável API_KEY e cole sua chave entre as aspas:

```Python

# Arquivo: config.py

# Cole sua chave AQUI ↓
API_KEY = "COLE_SUA_CHAVE_DO_GOOGLE_AQUI"
```


## ▶️ Como Rodar
Com as dependências instaladas e a chave configurada, execute o comando:

```Bash

python main.py
```
Após alguns segundos, o terminal exibirá um link local (geralmente http://127.0.0.1:7860). Clique nele para abrir o Tutor no seu navegador.

## 🧩 Como Usar
1. Escolha a Rotina: Ao iniciar, selecione se deseja treinar a "Redação Completa" ou apenas uma parte (ex: "Apenas Introdução").

2. Defina o Tema: Digite um tema, um eixo temático (ex: "Saúde") ou peça um tema "Aleatório".

3. Interaja:

-  O Tutor pedirá o planejamento ou a escrita do parágrafo.

-  Se a IA responder com dicas de melhoria, reescreva sua resposta.

-  O sistema só avançará para a próxima etapa quando seu texto estiver adequado.
