import matplotlib.pyplot as plt

for line in open('roads.txt'):
    points = [map(float, point.split(',')) for point in line.split(' ')]
    lons, lats = zip(*points)
    plt.plot(lons, lats, '-o', ms=3, mew=0, color='b')

plt.axis('equal')
plt.show()