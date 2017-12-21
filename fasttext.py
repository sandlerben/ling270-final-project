import gensim
import os
import logging
import itertools

from gensim.models.word2vec import Text8Corpus
from gensim.models.wrappers import FastText

MODEL_FILE = './phonmodels/model4'
TEXT8_FILE = './fil9_phon'
QUIZ_FILE = './questions-words-phon.txt'

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

if os.path.isfile(MODEL_FILE):
    model = FastText.load(MODEL_FILE)

else:
    corpus = Text8Corpus(TEXT8_FILE)
    # TODO: increase size and window *separately*
    model = FastText.train('./fasttext', corpus_file=TEXT8_FILE, size=300, window=10)
    model.save(MODEL_FILE)

model.accuracy(QUIZ_FILE)
