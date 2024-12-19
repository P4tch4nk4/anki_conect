from deep_translator import GoogleTranslator

translator = GoogleTranslator(source="en", target="pt", )


def translate(text):
    return translator.translate(text)
