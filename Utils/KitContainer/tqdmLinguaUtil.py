from deep_translator import GoogleTranslator
from tqdm import tqdm
 
class Translator:
    def __init__(self, source, target):
        self.source = source
        self.target = target

    def translate_text(self, text):
        translator = GoogleTranslator(source=self.source, target=self.target)
        translated_text = translator.translate(text)
        return translated_text


