from pumpkin_runner import run_with_timeout
import matplotlib.pyplot as plt

times=[1000,10000,20000,50000,100000]
results=[]
for t in times:
    results.append(run_with_timeout(t))
plt.plot(times,results)
plt.xlabel("Time taken(s)")
plt.ylabel("Best cost")
plt.gca().invert_yaxis()
plt.show()