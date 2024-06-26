import math
import numpy as np

# constants
# x, then y
list_to_coordinates = {0: (0, 0), 1: (1, 0), 2: (2, 0), 3: (3, 0), 4: (4, 0), 5: (5, 0), 6: (6, 0), 7: (7, 0),
                       8: (8, 0), 9: (9, 0), 10: (0, 1), 11: (1, 1), 12: (2, 1), 13: (3, 1), 14: (4, 1), 15: (5, 1),
                       16: (6, 1), 17: (7, 1), 18: (8, 1), 19: (9, 1), 20: (0, 2), 21: (1, 2), 22: (2, 2), 23: (3, 2),
                       24: (4, 2), 25: (5, 2), 26: (6, 2), 27: (7, 2), 28: (8, 2), 29: (9, 2)}
sfr_dist = 0.8  # sfb dist is 1, 1usfs 0.5
travel_dist = 0.05  # penalty for moving off of homerow when you aren't already there


class Finger:

    def __init__(self, name, history=None, speed=0):
        if history is None:
            history = np.array([(0, 0) for x in range(16)])   # good only for short-ish finger sequences
        self.name = name
        self.history = history
        self.speed = speed
        self.iter = 0

    # list comprehension fast apparently?
    # I guess we could try replacing lists with numpy arrays lol

    def press(self, index, time, freq):
        self.history[self.iter] = (index, time)
        if self.iter > 0:
            delta_time = time - self.history[self.iter - 1][1]

            distance = math.dist(list_to_coordinates[index], list_to_coordinates[self.history[self.iter - 1][0]])

            if distance > 0:
                speed_gain = (distance / (2 ** (delta_time - 1)))
            #  print(str(self.name) + " : " + "Speed gain: " + str(speed_gain) + " History: " + str(self.history))
            else:
                speed_gain = (sfr_dist / (2 ** (delta_time - 1)))
            # print(str(self.name) + " : " + "Speed gain SFR: " + str(speed_gain) + " History: " + str(self.history))
            self.speed = self.speed + (speed_gain * freq)
        else:
            if list_to_coordinates[index][1] != 1:
                self.speed = self.speed + (travel_dist * freq)
        self.iter += 1

    def __repr__(self):
        return self.name

    def clear_history(self):
        self.iter = 0
