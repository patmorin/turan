# Create a sequence with no arithmetic progress of length 3
from __future__ import division

import matplotlib.pyplot as plt

n = 30

nap = [1,2]
for x in range(3,n+1):
    try:
        for i in range(len(nap)-1):
            for j in range(i, len(nap)):
                if x-nap[j] == nap[j]-nap[i]:
                    raise Exception()
    except Exception:
        pass
    else:
        nap.append(x) 

print("X={}".format(nap))

plt.xticks(range(1, n+1))
plt.yticks(range(1, n+1))
plt.grid(True)
for a in range(1,n+1):
    data = [(a+x, a+2*x) for x in nap if a+2*x <= n]
    if data: 
        xdata, ydata = zip(*data)
        plt.plot(xdata, ydata, 'o-', markersize=25)
    # print("M{} = {}".format(a, [(a+x, a+2*x) for x in nap]))

plt.show()

