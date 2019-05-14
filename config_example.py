import os

BASE_PATH = os.path.dirname(__file__)

DATA_DIRNAME = 'data'
DATA_PATH = os.path.join(BASE_PATH, DATA_DIRNAME)

DICTIONARY_FILENAME = 'sentiwordnet.txt'
DICTIONARY_PATH = os.path.join(DATA_PATH, DICTIONARY_FILENAME)

