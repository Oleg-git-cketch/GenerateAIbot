import telebot
import requests
import io
from googletrans import Translator

TELEGRAM_TOKEN = "7545681011:AAFw7bbmAMjjQBWwVay0sEDgi-R_wJB_wxk"
STABILITY_KEY = "sk-3hfMRnb13SESUrFlKszX1oq31bttQ4DpAqb8tHL0fQVdkbmX"

bot = telebot.TeleBot(TELEGRAM_TOKEN)
translator = Translator()

def translate_to_english(text):
    try:
        translation = translator.translate(text, dest='en')
        return translation.text
    except Exception as e:
        print(f"Ошибка перевода: {e}")
        return text

@bot.message_handler(commands=['start'])
def start(msg):
    bot.send_message(msg.chat.id, "👋 Привет! Напиши, что ты хочешь увидеть, и я сгенерирую картинку ✨")

@bot.message_handler(func=lambda m: True)
def gen(msg):
    original_prompt = msg.text
    prompt = translate_to_english(original_prompt)

    bot.send_message(msg.chat.id, f"🎨 Генерирую изображение по запросу:\n«{original_prompt}»")

    files = {
        "prompt": (None, prompt),
        "model": (None, "sd3"),
        "mode": (None, "text-to-image"),
        "aspect_ratio": (None, "1:1"),
        "seed": (None, "0"),
        "output_format": (None, "png")
    }

    try:
        resp = requests.post(
            "https://api.stability.ai/v2beta/stable-image/generate/sd3",
            headers={
                "Authorization": f"Bearer {STABILITY_KEY}",
                "Accept": "image/*"
            },
            files=files,
            timeout=60
        )

        if resp.status_code == 200:
            bot.send_photo(msg.chat.id, io.BytesIO(resp.content))
        else:
            bot.send_message(msg.chat.id, f"❌ Ошибка {resp.status_code}:\n{resp.text}")

    except Exception as e:
        bot.send_message(msg.chat.id, f"⚠️ Произошла ошибка при обращении к API: {e}")

bot.polling()
