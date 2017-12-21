# LING270 Final Project

For this project, I trained three neural network models on English Wikipedia and benchmarked their performance on questions-words.txt. Read my final paper [here](https://drive.google.com/file/d/14Bv2nfm5o_JLPmnNiaPKqBDa0MqYGaCu/view?usp=sharing).

This repository contains the source code used.

## Setting up

##### Clone the repo

```
$ git clone https://github.com/sandlerben/ling270-final-project.git
$ cd ling270-final-project
```

##### Initialize a virtualenv

```
$ pip install virtualenv
$ virtualenv -p /path/to/python3.x/installation env
$ source env/bin/activate
```

##### Install the dependencies

```
$ pip install -r requirements.txt
```

##### Generate fil9

Follow instructions [here](http://mattmahoney.net/dc/textdata.html#appendixa).

##### Download CMUDict

```
$ wget http://svn.code.sf.net/p/cmusphinx/code/trunk/cmudict/cmudict-0.7b
```

##### Phonetically transcribe fil9 using CMUDict

```
$ python make_phonetic_corpus_and_questions.py
```

##### Train models

Modify the global variables in `standard_word2vec.py` and `fasttext.py`. Note that for FastText to work, it must be installed separately (see instructions [here](https://github.com/facebookresearch/fastText)).
