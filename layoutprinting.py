import pickle

with open('optimized_layout.pickle', 'rb') as f:
    layout = pickle.load(f)

with open('final_layout.txt', 'w') as f:
    f.write(layout.__repr__())