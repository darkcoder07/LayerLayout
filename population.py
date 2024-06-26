import pickle

import layoutgaming

def gen_random_layout():

    blank = layoutgaming.Layout([layoutgaming.Layer() for i in range(30)])

    with open('mr_clean_bigrams.pickle', 'rb') as g:
        mr_bigrams = dict(pickle.load(g))
        for key in mr_bigrams:
            blank.add_random_bigram(key)

    return blank

random_layout = gen_random_layout()
print(random_layout)

with open('initial_layout.txt', 'w') as f:
    f.write(gen_random_layout().__repr__())

