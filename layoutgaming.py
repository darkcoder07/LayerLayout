import random

import numpy as np
import fingers

# constants
empty = "__"
layer_size = 30

# defaults

defaultfingerdict = {0: "lp", 1 : "lr", 2: "lm", 3: "li", 4: "li", 5: "ri", 6: "ri", 7: "rm", 8: "rr", 9: "rp", 10: "lp",
                     11: "lr", 12: "lm", 13: "li", 14: "li", 15: "ri", 16: "ri", 17: "rm", 18: "rr", 19: "rp", 20: "lp",
                     21: "lr", 22: "lm", 23: "li", 24: "li", 25: "ri", 26: "ri", 27: "rm", 28: "rr", 29: "rp"}

defaultbase = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o",
               "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "'", ",", ".", ";"]

# default position can be an array like
defaultpos = np.array([0, 0])  # top left pinky
# bigrams will be a 3x10 matrix of bigrams
defaultbigrams = np.full((3, 10), "__")
print(defaultbigrams)


# LISTS
class Layout:

    def __init__(self, layer_list, base_layer=defaultbase, fingermap=defaultfingerdict):
        self.fingermap = defaultfingerdict
        self.layer_list = layer_list
        self.base_layer = defaultbase

        for finger in set(val for val in self.fingermap.values()):
            if finger == "lp":
                self.lp = fingers.Finger("lp")
            elif finger == "lr":
                self.lr = fingers.Finger("lr")
            elif finger == "lm":
                self.lm = fingers.Finger("lm")
            elif finger == "li":
                self.li = fingers.Finger("li")
            elif finger == "ri":
                self.ri = fingers.Finger("ri")
            elif finger == "rm":
                self.rm = fingers.Finger("rm")
            elif finger == "rr":
                self.rr = fingers.Finger("rr")
            elif finger == "rp":
                self.rp = fingers.Finger("rp")
            elif finger == "t":
                self.t = fingers.Finger("t")

        for index in self.fingermap:
            if self.fingermap[index] == "lp":
                self.fingermap[index] = self.lp
            elif self.fingermap[index] == "lr":
                self.fingermap[index] = self.lr
            elif self.fingermap[index] == "lm":
                self.fingermap[index] = self.lm
            elif self.fingermap[index] == "li":
                self.fingermap[index] = self.li
            elif self.fingermap[index] == "ri":
                self.fingermap[index] = self.ri
            elif self.fingermap[index] == "rm":
                self.fingermap[index] = self.rm
            elif self.fingermap[index] == "rr":
                self.fingermap[index] = self.rr
            elif self.fingermap[index] == "rp":
                self.fingermap[index] = self.rp
            elif self.fingermap[index] == "t":
                self.fingermap[index] = self.t

    def swap_layers(self, index1, index2):
        self.layer_list[index1], self.layer_list[index2] = self.layer_list[index2], self.layer_list[index1]

    def swap_bases(self, index1=69, index2=69):
        if index1 == 69:
            a = self.get_random_base_index()
            b = self.get_random_base_index()
            self.base_layer[a], self.base_layer[b] = self.base_layer[b], self.base_layer[a]
        else:
            self.base_layer[index1], self.base_layer[index2] = self.base_layer[index2], self.base_layer[index1]

    def swap_interlayer_bigrams_random(self):
        layer1 = self.layer_list[self.get_random_layer_index()]
        layer2 = self.layer_list[self.get_random_layer_index()]
        l1index = layer1.get_random_index()
        l2index = layer2.get_random_index()
        layer1.bigram_list[l1index], layer2.bigram_list[l2index] = layer2.bigram_list[l2index], layer1.bigram_list[
            l1index]

    def add_random_bigram(self, bigram):
        while True:
            layer = self.layer_list[self.get_random_layer_index()]
            if layer.add_bigram(bigram):
                break

    def get_random_layer_index(self):
        return random.randrange(0, len(self.layer_list))

    def get_random_base_index(self):
        return random.randrange(0, len(self.base_layer))

    def __repr__(self):
        representation = []
        index = 0
        for i in range(3):
            sublist = []
            for j in range(10):
                sublist.append(self.layer_list[index].matrix_rep())
                index = index + 1
            representation.append(sublist)
        return str(representation)


class Layer:

    def __init__(self, bigram_list=None):
        if bigram_list:
            self.bigram_list = bigram_list
        else:
            self.bigram_list = [empty for x in range(layer_size)]

    def swap_bigrams(self, index1=69, index2=69):
        if index1 == 69:
            a = self.get_random_index()
            b = self.get_random_index()
            self.bigram_list[a], self.bigram_list[b] = self.bigram_list[b], self.bigram_list[a]
        else:
            self.bigram_list[index1], self.bigram_list[index2] = self.bigram_list[index2], self.bigram_list[index1]

    def delete_bigram(self, index):
        self.bigram_list[index] = empty

    def add_bigram(self, bigram, index=69):
        if index != 69:
            self.bigram_list[index] = bigram
        else:  # this should only be used for initial random population...
            for i in range(1000):
                index = self.get_random_index()
                if self.bigram_list[index] == empty:
                    self.bigram_list[index] = bigram
                    return True

    def get_random_index(self):
        return random.randrange(0, len(self.bigram_list))

    def matrix_rep(self):
        representation = []
        index = 0
        for i in range(3):
            sublist = []
            for j in range(10):
                sublist.append(self.bigram_list[index])
                index = index + 1
            representation.append(sublist)
        return representation

    def __repr__(self):
        return str(self.matrix_rep())

    # meh stuff ngl
    def swap_bigrams_known(self, bigram1, bigram2):
        try:
            a, b = self.bigram_list.index(bigram1), self.bigram_list.index(bigram2)
            self.bigram_list[a], self.bigram_list[b] = self.bigram_list[b], self.bigram_list[a]
        except:
            print("Exception: One or both bigrams were not in this layer")

    # you should never be deleting a null bigram, so hopefully no duplication and the bigrams are unique lol
    def delete_bigram_known(self, bigram):
        try:
            index = self.bigram_list.index(bigram)
            self.bigram_list[index] = empty
            return index  # because we need this for uh, the interlayer swap
        except:
            print("Exception: Bigram deletion failed; maybe the bigram isn't in the layer?")


test_bigrams = [["ab", "ac", "ad", "ae", "af", "ag", "ah", "ai", "aj", "ak"],
                ["bb", "bc", "bd", "be", "bf", "bg", "bh", "bi", "bj", "bk"],
                ["cb", "cc", "cd", "ce", "cf", "cg", "ch", "ci", "cj", "ck"]]
