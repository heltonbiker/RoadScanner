#!/usr/bin/env python
# coding: utf-8

import matplotlib.pyplot as plt

with open('nodes.txt') as nodesfile:
    nodes = [(map(int, l.split(';'))) for l in nodesfile]
    nodesdict = {node[0] : (node[1], node[2]) for node in nodes}

with open('seeds.txt') as seedsfile:
    seeds = [(map(int, l.split(';'))) for l in seedsfile]

with open('edges.txt') as edgesfile:
    edges = [map(lambda x: nodesdict[int(x)], line.split(';')) for line in edgesfile]

for edge in edges:
    lats, lons = zip(*edge)
    plt.plot(lons, lats, 'k')




# # try to erase centers:
# from EnclosingCircle import make_circle
# from math import *

# def distance(p1, p2):
#     return hypot(p2[0] - p1[0], p2[1] - p1[1])

# clat, clon, radius = make_circle(seeds)

# plt.plot(clon, clat, 'o')

# seeds2 = []

# for seed in seeds:
#     d = distance(seed, (clat, clon))
#     print d
#     if d > radius*0.5:
#         seeds2.append(seed)

# slat2, slon2 = zip(*seeds2)
# plt.scatter(slon2, slat2, color='g', s=40, linewidths=0, alpha=1)


# lats, lons = zip(*nodes)
# plt.scatter(lons, lats, color='b', s=5, linewidths=0, alpha=0.05)

slat, slon = zip(*seeds)
plt.scatter(slon, slat, color='r', s=20, linewidths=0, alpha=1)

plt.axis('equal')
plt.grid()
plt.show()