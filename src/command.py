import config
import sys

from src.sentiment import SentimentAnalysis



class App:

    def __init__(self):
        self.dictionary_path = config.DICTIONARY_PATH
        self.analyser = SentimentAnalysis(config.DICTIONARY_PATH)

    def routes(self):
        return (
            self.analyse_single,
            self.analyse_file
        )

    def analyse_single(self):
        text = input("Print your text (en) here : ")
        result = self.analyser.score(text)

        formatted_output = "The result from -1 to 1 is : {}".format(result)
        print(formatted_output)
        print("\n")
        self.run()

    def analyse_file(self):
        print("future file analysis")

    def run(self):
        print("That do you suppose to do?")
        print("[0] - input single phrase")
        print("[1] - analyse file")
        print("[:q] - exit")

        action = None
        while action not in ('0', '1'):
            action = input("Select option: ")
            if action in ('q', ':q', 'quit'):
                sys.exit(1)

        routes = self.routes()
        routes[int(action)]()
