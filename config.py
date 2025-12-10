
import google.generativeai as genai

API_KEY = "Sua_API_Key_Aqui"

def setup_model():
    try:
        genai.configure(api_key=API_KEY)
    except Exception as e:
        print(f"⚠️ Erro ao carregar API Key: {e}")
        return None

    generation_config = {
        "temperature": 0.7,
        "top_p": 0.95,
        "max_output_tokens": 8192,
    }

    # Seleção de modelo resiliente
    model_name = "gemini-2.5-flash"
    try:
        available_models = [m.name for m in genai.list_models()]
        if "models/gemini-2.5-flash" in available_models:
            model_name = "gemini-2.5-flash"
        elif "models/gemini-pro" in available_models:
            model_name = "gemini-pro"
        else:
            for m in genai.list_models():
                if 'generateContent' in m.supported_generation_methods:
                    model_name = m.name
                    break
        print(f"✅ Modelo selecionado: {model_name}")
    except Exception as error:
        print(f"⚠️ Aviso na seleção: {error}. Usando padrão.")
        model_name = "gemini-pro"

    return genai.GenerativeModel(
        model_name=model_name,
        generation_config=generation_config,
    )


model = setup_model()