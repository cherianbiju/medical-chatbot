# chatbot_app/modules/multilingual.py

from langdetect import detect
from googletrans import Translator

translator = Translator()

def detect_language(text):
    try:
        return detect(text)
    except:
        return "en"  # fallback to English

def translate_to_english(text, lang):
    if lang != "en":
        try:
            return translator.translate(text, src=lang, dest='en').text
        except:
            return text
    return text

def translate_from_english(text, target_lang):
    if target_lang != "en":
        try:
            return translator.translate(text, src='en', dest=target_lang).text
        except:
            return text
    return text
