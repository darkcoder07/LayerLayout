import cProfile
import pstats
import copy
import pickle
from random import random
import scoring
import population


def optimize():
    random_layout = population.gen_random_layout()
    attempts = 0
    best_score = scoring.score(random_layout)

    while attempts < 100:
        new_score = 0
        temp_layout = copy.deepcopy(random_layout)
        random_num = random()
        if 0.75 > random_num > 0.3:
            temp_layout.swap_interlayer_bigrams_random()
        elif random_num < 0.3:
            temp_layout.swap_bases()
        else:
            temp_layout.layer_list[temp_layout.get_random_layer_index()].swap_bigrams()
        new_score = scoring.score(temp_layout)
        if new_score < best_score:
            attempts = 0
            best_score = new_score
            random_layout = copy.deepcopy(temp_layout)
        else:
            attempts = attempts + 1
            print("Couldn't find a better layout: " + str(attempts) + " attempts.")
            print(best_score)

    optimized_layout = random_layout
    print(optimized_layout)

    with open('optimized_layout.pickle', 'wb') as f:
        pickle.dump(optimized_layout, f)

with cProfile.Profile() as profile:
    optimize()

results = pstats.Stats(profile)
results.sort_stats(pstats.SortKey.TIME)
results.print_stats()
results.dump_stats("results.prof")
