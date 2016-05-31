import matplotlib.pyplot as plt

for line in open('roads.txt'):
    points = [map(float, point.split(',')) for point in line.split(' ')]
    lons, lats = zip(*points)
    plt.plot(lons, lats)

plt.axis('equal')
plt.show()