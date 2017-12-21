import gensim
import os
import logging

from gensim.models.word2vec import Text8Corpus, Word2Vec

MODEL_FILE = './model5'
TEXT8_FILE = './fil9'
QUIZ_FILE = './questions-words.txt'

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

if os.path.isfile(MODEL_FILE):
    model = Word2Vec.load(MODEL_FILE)

else:
    corpus = Text8Corpus(TEXT8_FILE)
    model = Word2Vec(corpus, size=400, workers=4, min_count=10, window=10)
    model.save(MODEL_FILE)

# model.accuracy(QUIZ_FILE)

print(model.wv.most_similar(positive=['austrian', 'colombia'], negative=['austria']))
