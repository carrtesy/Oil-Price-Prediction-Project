import matplotlib.pyplot as plt
import numpy as np

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

smfile = open('sm.txt', 'r')

E = []
tau = []
sm = []

while True:
    line = smfile.readline()
    if not line:
        break
    else:
        words = line.split()
        _E, _tau, _sm = float(words[1][:-1]), float(words[3]), float(words[5])
        print(_E, _tau, _sm)
        print(words)
        E.append(_E)
        tau.append(_tau)
        sm.append(_sm)

E = np.array(E)
tau = np.array(tau)
sm = np.array(sm)

ax.plot_trisurf(E, tau, sm, cmap = 'viridis', edgecolor = 'none')
ax.set_xlabel("E")
ax.set_ylabel("tau")
ax.set_zlabel("SM")
ax.view_init(elev = 36, azim = -135)

plt.savefig("sm_3d.png")
plt.show()