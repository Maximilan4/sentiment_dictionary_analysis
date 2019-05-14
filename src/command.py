import config
from src.sentiment import SentimentAnalysis
import nltk


class App:

    def __init__(self):
        self.dictionary_path = config.DICTIONARY_PATH
        self.analyser = SentimentAnalysis(config.DICTIONARY_PATH)

    def run(self):
        result = self.analyser.score("абракадавра")
        print(result)

