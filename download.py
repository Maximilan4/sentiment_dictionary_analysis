import nltk
import ssl
from config import NLTK_DATA_PATH, NLTK_RU_LOCAl_DICT_PATH
from distutils.dir_util import copy_tree

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

result = copy_tree(NLTK_RU_LOCAl_DICT_PATH, NLTK_DATA_PATH)
print('Copied ru nltk data to {}'.format(NLTK_DATA_PATH))

nltk.download('stopwords')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')

