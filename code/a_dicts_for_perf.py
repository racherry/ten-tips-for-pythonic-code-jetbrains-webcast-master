# ############ DICTIONARY vs. LIST LOOKUP PERF #############
# Create by Michael Kennedy (@mkennedy)
#
# Overview:
# If you had a large set of data and you need to "find" a subset
# of elements by some value (equality not a computation, such as
# between two values), it is dramatically faster. See the output
# comments at the very end of this file for numbers.
#
# original gist at https://gist.github.com/mikeckennedy/56ce3fa641439b8f9de03b5a5f545650
#
import collections
import datetime
import random

import sys

DataPoint = collections.namedtuple("DataPoint", "id x y temp quality")


def main():
    # #############################
    print("Creating data...", end=' ')
    sys.stdout.flush()

    data_list = []
    random.seed(0)
    for d_id in range(500000):
        x = random.randint(0, 1000)
        y = random.randint(0, 1000)
        temp = random.randint(-10, 50)
        quality = random.random()
        data_list.append(DataPoint(d_id, x, y, temp, quality))

    print("done.")
    sys.stdout.flush()

    # #############################
    print("Simulating randomized data ...", end=' ')
    sys.stdout.flush()

    data_list.sort(key=lambda d: d.quality)

    print("done.")

    # Create a list of random IDs to locate without duplication
    interesting_ids = list({random.randint(0, len(data_list)) for _ in range(0, 100)})
    print("Creating {} interesting IDs to seek.".format(len(interesting_ids)))

    # #############################
    print("Locating data in list...", end=' ')
    sys.stdout.flush()

    t0 = datetime.datetime.now()
    interesting_points = []
    for i in interesting_ids:
        pt = find_point_by_id_in_list(data_list, i)
        interesting_points.append(pt)

    t1 = datetime.datetime.now()
    dt_list = (t1 - t0).total_seconds()

    print("done.")
    sys.stdout.flush()

    print("DT: {} sec".format(dt_list))
    print(interesting_points)

    # #############################
    t0 = datetime.datetime.now()

    print("Creating dictionary...", end='')
    data_lookup = {d.id: d for d in data_list}

    print("done.")
    sys.stdout.flush()

    print("Locating data in dictionary...", end=' ')
    sys.stdout.flush()

    #    t0 = datetime.datetime.now()
    interesting_points = []
    for i in interesting_ids:
        item = data_lookup[i]
        interesting_points.append(item)

    t1 = datetime.datetime.now()
    dt_dict = (t1 - t0).total_seconds()

    print("done.")
    sys.stdout.flush()

    print("DT: {} sec".format(dt_dict))
    print(interesting_points)
    print()
    print("Speedup from dict: {:,.0f}x".format(round(dt_list / dt_dict)))


def find_point_by_id_in_list(data_list, i):
    for d in data_list:
        if d.id == i:
            return d

    return None


if __name__ == '__main__':
    main()

# ################# TYPICAL OUTPUT ###################
# Python 3
# OS X, Macbook Pro
#
# Creating data... done.
# Sorting data... done.
# Creating 100 interesting IDs to seek.
# Locating data in list... done.
# DT: 7.339648 sec
# [DataPoint(id=244225, x=308, y=736, temp=15, quality=0.2616059911451657), ...]
# Creating dictionary...done.
# Locating data in dictionary... done.
# DT: 8e-05 sec
# [DataPoint(id=244225, x=308, y=736, temp=15, quality=0.2616059911451657), ...]
#
# Speedup from dict: 91,746x
