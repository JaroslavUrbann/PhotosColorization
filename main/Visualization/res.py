import matplotlib.pyplot as plt
import matplotlib
import numpy as np
matplotlib.rcParams.update({'font.size': 22})
data = np.load('res.npy')
# print(data)
x = list(map(int, list(data.item().keys())))
y = list(map(int, list(data.item().values())))

x = [i / 1000000 for i in x]
print(x)
print(len(x))
print(max(y))
plt.bar(x, y, align='center', width=1)
plt.yscale("log")
plt.xlabel('Rozlišení [Mpx]')
plt.ylabel('Počet obrázků')
fig = matplotlib.pyplot.gcf()
fig.set_size_inches(18.5, 10.5)
fig.savefig('test2png.png', dpi=100)
plt.show()
