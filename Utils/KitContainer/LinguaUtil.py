from deep_translator import GoogleTranslator

def translate_text(source, target, text):
    translator = GoogleTranslator(source=source, target=target)
    translated_text = translator.translate(text)
    return translated_text
