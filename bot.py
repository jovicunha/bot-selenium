import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# ===== PEGANDO VARIÁVEIS SECRETAS DO GITHUB =====
USERNAME = os.environ["LOGIN_USER"]
PASSWORD = os.environ["LOGIN_PASS"]
BOT_TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

# ===== CONFIGURAÇÃO CHROME HEADLESS =====
chrome_options = Options()
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--window-size=1920,1080")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

try:
    # ===== ABRIR PÁGINA DE PRESENÇA =====
    driver.get("https://campus.upecde.edu.py:5022/moodle/mod/attendance/view.php?id=325")
    time.sleep(3)

    # ===== LOGIN =====
    driver.find_element(By.ID, "username").send_keys(USERNAME)
    driver.find_element(By.ID, "password").send_keys(PASSWORD)
    driver.find_element(By.ID, "password").send_keys(Keys.RETURN)
    time.sleep(8)

    # ===== ATUALIZA A PÁGINA =====
    driver.refresh()
    time.sleep(3)

    # ===== AJUSTA JANELA PARA PRINT =====
    total_height = driver.execute_script("return document.body.scrollHeight")
    driver.set_window_size(1920, total_height)

    # ===== TIRA PRINT =====
    screenshot_path = "comprovante.png"
    driver.save_screenshot(screenshot_path)

    # ===== ENVIA FOTO PARA O TELEGRAM =====
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
    mensagem = "Sua presença em fisiologia foi registrada, segue comprovante!"
    with open(screenshot_path, "rb") as foto:
        requests.post(
            url,
            data={"chat_id": CHAT_ID, "caption": mensagem},
            files={"photo": foto}
        )

    print("Foto enviada com sucesso para o Telegram!")

finally:
    driver.quit()
