import os
import requests

# ===== VARIÁVEIS (do GitHub Secrets ou local) =====
BOT_TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

# ===== MENSAGEM =====
mensagem = "Oi 👋"

# ===== ENVIO =====
url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

requests.post(
    url,
    data={
        "chat_id": CHAT_ID,
        "text": mensagem
    }
)

print("Mensagem enviada!")
