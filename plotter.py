from pumpkin_runner import run_with_timeout
import matplotlib.pyplot as plt
# 112 69 66 54 41
# 143 461 339 265 819 984 1059
# 192 373 370 271 76 849 1103
r1=[143,461,339,265,819,984,1059]
r2=[192,373,370,271,761,859,1103]

plt.figure(figsize=(10, 6))
plt.plot(r1, label='Bumped idle times', marker='o')
plt.plot(r2, label='No bump', marker='o')

# Add labels and title
plt.xlabel('Index')
plt.ylabel('Values')
#plt.title('Plot of r1 and r2 Arrays')

# Add legend and grid
plt.legend()
plt.grid(True)

# Show the plot
plt.show()
'''
times=[1000,5000,10000,20000,40000]
results=[]
for t in times:
    print(t)
    val = run_with_timeout(t)
    print(val)
    results.append(val)
plt.plot(times,results)
plt.xlabel("Time taken(s)")
plt.ylabel("Best cost")
plt.gca().invert_yaxis()
plt.show()
'''