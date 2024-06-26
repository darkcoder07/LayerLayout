from collections import Counter
from itertools import islice
import re
import pickle

unshift_dict = str.maketrans('" :', "' ;")


def window(seq: str, n=2):
    # sliding window time
    it = iter(seq)
    result = tuple(islice(it, n))
    if len(result) == n:
        yield result
    for elem in it:
        result = result[1:] + (elem,)
        yield result


def process_corpus_words(file):
    processed_corpus = []
    with open(file, errors="ignore") as f:
        for line in f:
            lower = line.lower()
            words = lower.split()
            processed_corpus.extend(words)

    word_dict = dict(Counter(processed_corpus))
    return word_dict


# print(process_corpus_words("mr.txt"))

# credit to Pine and Eve for this thingy
def ngrams(text: str, n: int):
    grams = window(text, n=n)
    ngrams_out = Counter(''.join(x) for x in grams if not ' ' in x).most_common()
    return dict(ngrams_out)


def ngrams_from_file(file, n: int):
    ngram_dict = {}
    with open(file, errors="ignore") as f:
        for line in f:
            lower = line.lower().translate(unshift_dict)
            ngram_dict = Counter(ngram_dict) + Counter(ngrams(str(lower), n))
    return ngram_dict


ngram_list = ngrams_from_file("mr.txt", 2)


def clean_dict(input_dict):
    out_dict = input_dict.copy()
    for i in input_dict:
        if re.search("[^a-z,.';\s]", i):
            del out_dict[i]
    return out_dict


clean_ngram_list = clean_dict(ngram_list)
print(clean_dict(ngram_list))
print(len(clean_dict(ngram_list)))


def process_words_more(input_dict: dict):
    word_dict = input_dict
    for word in word_dict.copy():

        unshift = word.translate(unshift_dict)
        if not re.search("[^a-z,.';\s]", unshift):
            new_word = unshift + " "
        else:
            unspecial = re.sub("[^a-z,.';\s]", ' ', unshift)
            new_word = unspecial + " "

        word_dict[new_word] = word_dict.pop(word)
    return word_dict


def dict_to_file(input_dict: dict, file="default.pickle"):
    with open(file, 'wb') as f:
        pickle.dump(input_dict, f)


dict_to_file(clean_ngram_list, "mr_clean_bigrams.pickle")
dict_to_file(process_corpus_words("mr.txt"), "mr_words")
dict_to_file(process_words_more(process_corpus_words("mr.txt")), "mr_processed_words")

with open('mr_processed_words', 'rb') as f:
    processed_words = dict(pickle.load(f))
    thingy = processed_words.copy()
    for word in thingy:
        if thingy[word] < 4:
            processed_words.pop(word)
    with open('mr_more_processed_words', 'wb') as q:
        pickle.dump(processed_words, q)
