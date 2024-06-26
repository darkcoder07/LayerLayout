import pickle
import random
import layoutgaming

def score(layout: layoutgaming.Layout):
    bigrams_to_index = {}
    base_layer_index = {}
    total_speed = 0
    unique_fingers = set(layout.fingermap.values())

    for i in range(30):
        for j in range(layoutgaming.layer_size):
            bigrams_to_index[layout.layer_list[i].bigram_list[j]] = (i, j)
# can ALSO move to layout
    for i in range(30):
        base_layer_index[layout.base_layer[i]] = i

    with open('mr_more_processed_words', 'rb') as g:   # can maybe optimize
        processed_words = dict(pickle.load(g))

        # random.seed(10)
        # dict_slice = random.choices(list(processed_words.keys()), weights=processed_words.values(), k=500)
        # random.seed(None)
        for word in processed_words:
            freq = processed_words[word]
          #  print(str(word) + " : " + str(freq))
            t = 0
            while t + 2 <= len(word):
                chunk = word[t:t + 2]
                if chunk[0] == " ":
                    t = t + 1
                else:
                    if chunk[1] != " ":   # ditto lol, 2 only remember
                     #   print(chunk + " : " + str(bigrams_to_index[chunk]))
                     #   print(findfinger(bigrams_to_index[chunk][0], layout).name)
                     #   print(findfinger(bigrams_to_index[chunk][1], layout).name)
                        chunk_index = bigrams_to_index[chunk]
                        layout.fingermap[chunk_index[0]].press(chunk_index[0], t, freq)
                        t = t + 1
                        layout.fingermap[chunk_index[1]].press(chunk_index[1], t, freq)
                        t = t + 1
                    else:
                       # print(chunk + " : " + str(base_layer_index[chunk[0]]))
                      #  print(findfinger(base_layer_index[chunk[0]], layout))
                        base_chunk_index = base_layer_index[chunk[0]]
                        layout.fingermap[base_chunk_index].press(base_layer_index[chunk[0]], t, freq)
                        t = t + 2

            for finger in unique_fingers:
                finger.clear_history()

        for finger in unique_fingers:
            total_speed = total_speed + finger.speed
            finger.speed = 0

        return total_speed


# random_layout = population.gen_random_layout()
# print(score(random_layout))

"""if not re.search(' ', chunk):
                      layout.fingermap[bigrams_to_index[chunk][0]].press(bigrams_to_index[chunk][0], t)  # this is actually so terrible
                      t = t + 1
                      layout.fingermap[bigrams_to_index[chunk][1]].press(bigrams_to_index[chunk][1], t)
                      t = t + 1
                  else:  # spacegram
                      layout.fingermap[base_layer_index[chunk[0]]].press(base_layer_index[chunk[0]], t)
                      t = t + 2 
          for finger in set(layout.fingermap):
              finger.clear_history()

      for finger in layout.fingermap:
          total_speed = total_speed + finger.speed"""

#with open('optimized_layout.pickle', 'rb') as f:
   # optimized_layout = pickle.load(f)
   # print(optimized_layout)
   # print(score(optimized_layout))
   # print(optimized_layout.base_layer)

with open('mr_processed_words', 'rb') as f:
    dictthing = dict(pickle.load(f))
 #   for word in dictthing:
      #  print(word)

#optimized_layout.layer_list[0].delete_bigram(10)
  #  optimized_layout.layer_list[0].add_bigram("ez", 10)
   # optimized_layout.layer_list[17].delete_bigram(24)
    #optimized_layout.layer_list[17].add_bigram("ma")