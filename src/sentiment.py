import nltk
import re

from src import average
from src.parser import TextChunk


class SentimentAnalysis(object):

    def __init__(self, filename, weighting='geometric'):
        """Проверка правильности выбора механизма подсчета среднего значения"""
        if weighting not in ('geometric', 'harmonic', 'average'):
            raise ValueError(
                'Allowed weighting options are geometric, harmonic, average')
        # конвертируем файл словаря во внутренние типы, для удобства работы
        self.swn_pos = {'a': {}, 'v': {}, 'r': {}, 'n': {}}
        self.swn_all = {}
        self.build_swn(filename, weighting)
        # https://pythonprogramming.net/natural-language-toolkit-nltk-part-speech-tagging/ - список тегов nltk
        self.impt = {'NNS', 'NN', 'NNP', 'NNPS', 'JJ', 'JJR', 'JJS',
                    'RB', 'RBR', 'RBS', 'VB', 'VBD', 'VBG', 'VBN',
                    'VBP', 'VBZ', 'unknown'}
        self.non_base = {'VBD', 'VBG', 'VBN', 'VBP', 'VBZ', 'NNS', 'NNPS'}
        self.negations = {'not', 'n\'t', 'less', 'no', 'never',
                         'nothing', 'nowhere', 'hardly', 'barely',
                         'scarcely', 'nobody', 'none'}

    def build_swn(self, filename, weighting):
        """Построчно бежим по файлу"""
        records = [line.split('\t') for line in open(filename)]
        for rec in records:
            # получаем слово/слова и его принадлежность
            words = rec[4].split()
            pos = rec[0]

            # получаем оценку чувствительности, записываем результаты в словарь, предварительно посчитав разницу
            # положительной и отрицательной оценки слова
            # пример {'a' : {'able':{1:0.125, 2: 0.125, 4 : 0.25}}}
            for word_num in words:
                word = word_num.split('#')[0]
                sense_num = int(word_num.split('#')[1])

                if word not in self.swn_pos[pos]:
                    self.swn_pos[pos][word] = {}
                self.swn_pos[pos][word][sense_num] = float(
                    rec[2]) - float(rec[3])
                if word not in self.swn_all:
                    self.swn_all[word] = {}
                self.swn_all[word][sense_num] = float(rec[2]) - float(rec[3])

        # считаем среднее значение оценки окраски слова, опираясь на выбранный механизм подсчета
        for pos in self.swn_pos.keys():
            for word in self.swn_pos[pos].keys():
                # через генераторное выражение, заполняем список коэфициентов, учитывая чувствительность (ключ словаря)
                newlist = [self.swn_pos[pos][word][k] for k in sorted(
                    self.swn_pos[pos][word].keys())]
                if weighting == average.ARITHMETIC:
                    self.swn_pos[pos][word] = average.arithmetic(newlist)
                if weighting == average.GEOMETRIC_WEIGHTED:
                    self.swn_pos[pos][word] = average.geometric_weighted(newlist)
                if weighting == average.HARMONIC_WEIGHTED:
                    self.swn_pos[pos][word] = average.harmonic_weighted(newlist)

        # тоже самое проделываем для общего словаря
        for word in self.swn_all.keys():
            newlist = [self.swn_all[word][k] for k in sorted(
                self.swn_all[word].keys())]
            if weighting == average.ARITHMETIC:
                self.swn_all[word] = average.arithmetic(newlist)
            if weighting == average.GEOMETRIC_WEIGHTED:
                self.swn_all[word] = average.geometric_weighted(newlist)
            if weighting == average.HARMONIC_WEIGHTED:
                self.swn_all[word] = average.harmonic_weighted(newlist)

    def pos_short(self, pos):
        """Конвертим тег NLTK в корректный формат"""
        if pos in set(['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']):
            return 'v'
        elif pos in set(['JJ', 'JJR', 'JJS']):
            return 'a'
        elif pos in set(['RB', 'RBR', 'RBS']):
            return 'r'
        elif pos in set(['NNS', 'NN', 'NNP', 'NNPS']):
            return 'n'
        else:
            return 'a'

    def score_word(self, word, pos):
        """Получаем обощенную оценку эмоциональной окраски слова"""
        try:
            return self.swn_pos[pos][word]
        except KeyError:
            try:
                return self.swn_all[word]
            except KeyError:
                return 0

    def score_chunk(self, chunk: TextChunk):
        """Получаем эмоциональную окраску одного куска текста (оценивается каждое предложение)"""
        rates = []
        for sentence in chunk.sentences:
            rates.append(self.score(sentence))

        return average.arithmetic(rates)

    def score(self, sentence):
        """Получаем эмоциональную окраску предложения"""

        stopwords = nltk.corpus.stopwords.words('english')
        wnl = nltk.WordNetLemmatizer()

        scores = []
        # бьем предложение на слова
        tokens = nltk.tokenize.word_tokenize(sentence)
        # получаем nltk теги по словам
        tagged = nltk.pos_tag(tokens)

        index = 0
        for el in tagged:

            pos = el[1]
            try:
                word = re.match('(\w+)', el[0]).group(0).lower()
                start = index - 5
                if start < 0:
                    start = 0
                neighborhood = tokens[start:index]

                # формируем возможные списки устойчивых фраз
                word_minus_one = tokens[index-1:index+1]
                word_minus_two = tokens[index-2:index+1]

                # Если устойчивое выражение есть в общем словаре, считаем его единым словом
                if self.is_multiword(word_minus_two):
                    if len(scores) > 1:
                        scores.pop()
                        scores.pop()
                    if len(neighborhood) > 1:
                        neighborhood.pop()
                        neighborhood.pop()
                    word = '_'.join(word_minus_two)
                    pos = 'unknown'

                elif self.is_multiword(word_minus_one):
                    if len(scores) > 0:
                        scores.pop()
                    if len(neighborhood) > 0:
                        neighborhood.pop()
                    word = '_'.join(word_minus_one)
                    pos = 'unknown'

                # Получение конкретной оценки из SentiWordNet
                if (pos in self.impt) and (word not in stopwords):
                    if pos in self.non_base:
                        word = wnl.lemmatize(word, self.pos_short(pos))
                    score = self.score_word(word, self.pos_short(pos))
                    if len(self.negations.intersection(set(neighborhood))) > 0:
                        score = -score
                    scores.append(score)

            except AttributeError:
                pass

            index += 1

        return average.arithmetic(scores)

    def is_multiword(self, words):
        """Проверяем, есть ли набор слов в словаре как устойчевое выражение"""
        joined = '_'.join(words)
        return joined in self.swn_all
