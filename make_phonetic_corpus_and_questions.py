from functools import lru_cache
from itertools import product as iterprod
import timeout_decorator

CMUDICT_PATH = './cmudict-0.7b'
INPUT_PATH = './fil9'
QUESTIONS_INPUT_PATH = './questions-words.txt'
QUESTIONS_OUTPUT_PATH = './questions-words-phon.txt'
OUTPUT_PATH = './fil9_phon'

# first, read cmu dict into memory

cmu_dict = {} # word -> list of phonemes

with open(CMUDICT_PATH, mode='r', encoding='latin-1') as f:
    for line in f:
        line = line.strip()
        if line.startswith(';'):
            continue
        line_split = line.split('  ')
        cmu_dict[line_split[0]] = line_split[1].split(' ')

# TODO: make sure the model is case insensitive
two_letter_to_one = {
    'AA': 'a',
    'AE': '@',
    'AH': 'A',
    'AO': 'c',
    'AW': 'W',
    'AX': 'X',
    'AY': 'Y',
    'EH': 'E',
    'ER': 'R',
    'EY': 'e',
    'IH': 'I',
    'IX': 'X',
    'IY': 'i',
    'OW': 'o',
    'OY': 'O',
    'UH': 'U',
    'UW': 'u',
    'B': 'b',
    'CH': 'C',
    'D': 'd',
    'DH': 'D',
    'DX': 'F',
    'EL': 'L',
    'EM': 'M',
    'EN': 'N',
    'F': 'f',
    'G': 'g',
    'HH': 'h',
    'JH': 'J',
    'K': 'k',
    'L': 'l',
    'M': 'm',
    'N': 'n',
    'NG': 'G',
    'P': 'p',
    'Q': 'Q',
    'R': 'r',
    'S': 's',
    'SH': 'S',
    'T': 't',
    'TH': 'T',
    'V': 'v',
    'W': 'w',
    'WH': 'H',
    'Y': 'y',
    'Z': 'z',
    'ZH': 'Z'
}

cmu_dict_prime = {}

def two_to_one(ph):
    if ph.endswith('0') or ph.endswith('1') or ph.endswith('2'):
        ph = ph[:-1]
    return two_letter_to_one[ph]

for word in cmu_dict.keys():
    phones = cmu_dict[word]
    phones_prime = ''.join(list(map(two_to_one, phones)))
    cmu_dict_prime[word] = phones_prime

# second, transform fil9

@timeout_decorator.timeout(120)
@lru_cache(maxsize=131072)
def wordbreak(s):
    if s in cmu_dict_prime:
        return cmu_dict_prime[s]
    middle = len(s)/2
    partition = sorted(list(range(len(s))), key=lambda x: (x-middle)**2-x)
    for i in partition:
        pre, suf = (s[:i], s[i:])
        suf_call = wordbreak(suf)
        if pre in cmu_dict_prime and suf_call is not None:
            # return [x+y for x,y in iterprod(cmu_dict_prime[pre], wordbreak(suf))]
            print(pre, suf)
            return cmu_dict_prime[pre] + suf_call
    return None

new_output = []
success_found = 0
not_found = 0

count = 0

with open(INPUT_PATH, mode='r') as f:
    # TODO: this is very memory inefficient, use a buffer
    entire_file = f.read()
    all_words = entire_file.split(' ')
    len_all = len(all_words)
    len_distinct = len(set(all_words))
    print('{} words, {} distinct'.format(len_all, len_distinct))

    for word in all_words:
        word = word.upper()
        if word in cmu_dict_prime:
            new_output.append(cmu_dict_prime[word])
            success_found += 1
        elif word == '':
            continue
        else:
            not_found += 1

            try:
                synth_word = wordbreak(word)
            except Exception as e:
                print('got error on {}'.format(word))
                continue

            new_output.append(synth_word)

        count += 1
        if count % 100000 == 0:
            print(count / len_all)

print('{} words were in cmudict, {} synthetic were used'.format(success_found, not_found))

with open(OUTPUT_PATH, mode='w') as f:
    f.write(' '.join(new_output))

with open(QUESTIONS_INPUT_PATH, mode='r') as r, open(QUESTIONS_OUTPUT_PATH, mode='w') as w:
    for line in r:
        if line.startswith(':'):
            w.write(line)
        else:
            line = line.upper()
            splt = line.strip().split(' ')
            splt_prime = map(wordbreak, splt)
            w.write(' '.join(splt_prime) + '\n')
