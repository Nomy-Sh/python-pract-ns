# from transformers import pipeline

# # Set up translation pipelines
# translation_hindi_to_english = pipeline("translation_hi_to_en", model="Helsinki-NLP/opus-mt-hi-en")
# translation_english_to_hindi = pipeline("translation_en_to_hi", model="Helsinki-NLP/opus-mt-en-hi")

# # Example: Translate from Hindi to English
# hindi_text = "mera naam noman hai" #"नमस्ते, कैसे हो आप?"
# translated_text_hi_to_en = translation_hindi_to_english(hindi_text, max_length=50)[0]['translation_text']
# print(f"Hindi to English: {translated_text_hi_to_en}")

# # Example: Translate from English to Hindi
# english_text = "Hello, how are you?"
# translated_text_en_to_hi = translation_english_to_hindi(english_text, max_length=50)[0]['translation_text']
# print(f"English to Hindi: {translated_text_en_to_hi}")




# from transformers import pipeline

# # Translation pipeline setup
# translation_hindi_to_english = pipeline("translation_hi_to_en", model="Helsinki-NLP/opus-mt-hi-en")

# # Example: Translate from Hindi to English
# hindi_text = "mai abhi jis bhasha me bat karra hu ise kya kahte hai?"
# translated_text_hi_to_en = translation_hindi_to_english(hindi_text, max_length=50)[0]['translation_text']
# print(f"Hindi to English: {translated_text_hi_to_en}")





# from googletrans import Translator

# def translate_text(text, src_lang, dest_lang):
#     translator = Translator()
#     translated_text = translator.translate(text, src=src_lang, dest=dest_lang).text
#     return translated_text

# # Example: Translate from Hindi to English
# hindi_text = "aur ye batao kya tum meri bat samajh rahe ho?"
# translated_text_hi_to_en = translate_text(hindi_text, src_lang='hi', dest_lang='en')
# print(f"Hindi to English: {translated_text_hi_to_en}")


from mtranslate import translate

def translate_text_offline(text, dest_lang):
    translated_text = translate(text, dest_lang)
    return translated_text

# Example: Translate from Hindi to English (offline)
hindi_text = "mai abhi jis bhasha me bat karra hu ise kya kahte hai?"
translated_text_hi_to_en_offline = translate_text_offline(hindi_text, dest_lang='en')
print(f"Hindi to English (offline): {translated_text_hi_to_en_offline}")
