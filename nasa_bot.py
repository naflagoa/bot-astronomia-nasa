import requests
from deep_translator import GoogleTranslator

NASA_API_KEY = ""
TELEGRAM_TOKEN = ""
CHAT_ID = ""

def buscar_dados_nasa():
    """Busca a foto do dia e a explicação na API da NASA."""
    print("Acessando a NASA...")
    # AQUI ESTAVA O ERRO: Use o nome da variável NASA_API_KEY
    url = f"https://api.nasa.gov/planetary/apod?api_key={NASA_API_KEY}&date=2026-01-01"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None

def traduzir_texto(texto):
    """Traduz o texto do Inglês para o Português."""
    print(" Traduzindo explicação...")
    return GoogleTranslator(source='en', target='pt').translate(texto)

def enviar_para_telegram(titulo, imagem_url, legenda):
    """Envia a foto e a legenda para o Telegram."""
    print(" Enviando para o celular...")
    url_telegram = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto"
    
    mensagem = f"✨ *{titulo}* ✨\n\n{legenda}"
    if len(mensagem) > 1024:
        mensagem = mensagem[:1020] + "..."

    payload = {
        "chat_id": CHAT_ID,
        "photo": imagem_url,
        "caption": mensagem,
        "parse_mode": "Markdown"
    }
    requests.post(url_telegram, data=payload)

# --- EXECUÇÃO ---
if __name__ == "__main__":
    dados = buscar_dados_nasa()
    if dados and dados.get('media_type') == 'image':
        t_pt = traduzir_texto(dados['title'])
        l_pt = traduzir_texto(dados['explanation'])
        enviar_para_telegram(t_pt, dados['url'], l_pt)
        print("Sucesso! Olhe seu Telegram.")
    else:
        print("Hoje não há imagem disponível (pode ser vídeo).")