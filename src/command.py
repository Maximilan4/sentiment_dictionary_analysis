import config
import sys

from src.average import ARITHMETIC, HARMONIC_WEIGHTED, GEOMETRIC_WEIGHTED, arithmetic
from src.sentiment import SentimentAnalysis
from src.translator import GoogleTranslator
from src.parser import TextParser, TextChunk


class App:

    def __init__(self):
        self.dictionary_path = config.DICTIONARY_PATH
        self.analyser = SentimentAnalysis(config.DICTIONARY_PATH, GEOMETRIC_WEIGHTED)
        self.translator = GoogleTranslator()
        self.parser = TextParser()

    def routes(self):
        return (
            self.analyse_single,
            self.analyse_file
        )

    def analyse_single(self):
        text = input("Введите текст : ")

        rates = []
        for chunk in self.parser.build_chunks(text):
            translated = self.translator.translate(str(chunk))
            en_chunk = TextChunk.from_text(translated)
            rates.append(self.analyser.score_chunk(en_chunk))

        rate = arithmetic(rates)
        formatted_output = "Оценка : {}".format(rate)
        print(formatted_output)
        print("\n")
        self.run()

    def analyse_file(self):
        print("future file analysis")

    def run(self):
        print("Что делаем?")
        print("[0] - посчитать эмоциональную окраску одной фразы")
        print("[1] - посчитать эмоциональную окраску текста (файл)")
        print("[:q] - выйти")

        action = 0
        while action not in ('0', '1'):
            action = input("Опция: ")
            if action in ('q', ':q', 'quit'):
                sys.exit(1)

        routes = self.routes()
        routes[int(action)]()
