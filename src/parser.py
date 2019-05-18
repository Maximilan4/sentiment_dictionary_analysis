import nltk
import re
import io
from src import TEXT_CHUNK_SIZE
from nltk.tokenize import sent_tokenize
from pathlib import Path


class TextParser:
    """Методы для разбиение текста на части"""
    def parse_file(self, path):
        """Считываем текст из файла"""
        path = Path(path)
        text = []

        if not path.is_file():
            return False

        with open(file=str(path), mode='r', encoding='utf-8', errors='replace') as lines:
            for line in lines:
                text.append(line)

        return ''.join(text)

    def build_chunks_from_file(self, path):
        text = self.parse_file(path)
        if not text:
            return False

        yield from self.build_chunks(text)

    def build_chunks(self, text: str):
        text = re.sub('[\'\"\n`-]', '', text)

        tokenizer = nltk.data.load('tokenizers/punkt/russian.pickle')
        sentences = tokenizer.tokenize(text)
        sentences.reverse()

        chunk = TextChunk()

        while len(sentences) > 0:
            sentence = sentences.pop()
            if chunk.append(sentence):
                continue
            else:
                yield chunk
                chunk = TextChunk()
                chunk.append(sentence)

        yield chunk


class TextChunk:
    """
    Класс, содержащий в себе массив предложений, длина которых в сумме не превышает 15000 символов
    """
    def __init__(self):
        self.sentences = []
        self.free_space = TEXT_CHUNK_SIZE

    def append(self, sentence):
        sentence_length = len(sentence)
        if sentence_length <= self.free_space:
            self.sentences.append(sentence)
            self.free_space -= sentence_length
        else:
            return False

        return True

    @classmethod
    def from_text(cls, text):
        sentences = sent_tokenize(text)
        chunk = cls()
        for sentence in sentences:
            if chunk.append(sentence):
                continue
            else:
                return chunk

        return chunk

    def __str__(self):
        return ''.join(self.sentences)
