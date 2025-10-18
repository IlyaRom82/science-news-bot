import requests

TOKEN = "8258197340:AAG1z4Bfcs6AhL7sWMXTREYvSlQFdDos7i8"

try:
    url = f"https://api.telegram.org/bot{TOKEN}/getWebhookInfo"
    r = requests.get(url, timeout=10)  # таймаут 10 секунд
    print(r.json())
except requests.exceptions.RequestException as e:
    print("Ошибка запроса:", e)
