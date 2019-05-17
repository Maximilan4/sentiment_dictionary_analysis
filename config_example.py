import os

BASE_PATH = os.path.dirname(__file__)
HOME_DIR = os.path.expanduser('~')

DATA_DIRNAME = 'data'
DATA_PATH = os.path.join(BASE_PATH, DATA_DIRNAME)

DICTIONARY_FILENAME = 'sentiwordnet.txt'
DICTIONARY_PATH = os.path.join(DATA_PATH, DICTIONARY_FILENAME)

NLTK_RU_LOCAl_DICT_PATH = os.path.join(DATA_PATH, 'nltk_data')
NLTK_DATA_PATH = os.path.join(HOME_DIR, 'nltk_data')
