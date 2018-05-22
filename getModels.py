import json
from watson_developer_cloud import LanguageTranslatorV2 as LanguageTranslator

language_translator = LanguageTranslator(
username='d0d279bc-31a0-4468-ac0b-37118d36b4f7',
password='Qt4TvHYUNvdy')

models = language_translator.list_models()
print(json.dumps(models, indent=2))