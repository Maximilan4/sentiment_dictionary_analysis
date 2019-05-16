from googletrans import Translator, constants


class GoogleTranslator(Translator):

    CHARACTER_LIMIT = 15000

    def __init__(self, service_urls=None, user_agent=constants.DEFAULT_USER_AGENT,
                 proxies=None, timeout=None):
        self.default_language = 'en'
        super().__init__(service_urls, user_agent,
                         proxies, timeout)

    def translate(self, text, dest='en', src='auto'):
        if len(text) > self.CHARACTER_LIMIT:
            raise CharacterLimitException()

        detection = self.detect(text)
        if detection.lang == self.default_language:
            print("Перевод не требуется")
            return text

        translation_result = super().translate(text, dest, src)
        print("Оригинальный текст: {}".format(translation_result.origin))
        print("Переведено в : {}".format(translation_result.text))

        return translation_result.text


class CharacterLimitException(Exception):
    def __init__(self):
        self.message = "Превышен лимит в {} символов".format(GoogleTranslator.CHARACTER_LIMIT)
