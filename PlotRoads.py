import matplotlib.pyplot as plt

for line in open('roads.txt'):
    points = [map(float, point.split(',')) for point in line.split(' ')]
    lons, lats = zip(*points)
    plt.plot(lons, lats, '-o', mew=0, lw=2, alpha=0.5)

plt.axis('equal')
plt.show()