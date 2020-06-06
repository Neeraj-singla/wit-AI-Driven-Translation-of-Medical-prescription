import sys
from ibm_watson import LanguageTranslatorV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import json
def language_translator(input_text,target_language):
        api_key_translator = '{api-key}'
        url_translator = "{api-key}"
        authenticator = IAMAuthenticator(api_key_translator)
        language_translator = LanguageTranslatorV3(
        version='2020-06-03',
        authenticator=authenticator)
        language_translator.set_service_url(url_translator)
        language_translator.set_disable_ssl_verification(True)
        translation = language_translator.translate(
        text=input_text , target = target_language).get_result()
        results = json.dumps(translation, indent=2, ensure_ascii=False)
        return results

if __name__ == '__main__':
            result = language_translator("1 by mouth twice a day","hi")
            print(json.loads((result))["translations"][0])
