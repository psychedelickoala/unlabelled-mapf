import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

def f(a, l, n, k):
    if 0 < l < n:
        return (l**(l-1))*((n-l)**(n-l-1))*math.comb(n-k, l-a)
    return 0

def pr(l, n):
    return math.comb(n, l)*(l**(l-1))*((n-l)**(n-l-1))/(2*(n-1)*(n**(n-2)))

def expected_OPT(n, k):
    array = np.zeros(k+1)
    denom = n**(n-2)
    for a in range(k+1):
        array[a] = np.sum([f(a, l, n, k) for l in range(a, n-k+a+1)])*math.comb(k, a)

    sum = 0
    for a in range(k+1):
        for b in range(a+1, k+1):
            sum += (b-a)*array[a]*array[b]

    result = sum/(2*(n-1)*(denom**2))
    print(f"expected_OPT(n={n}, k={k}) = {result}")
    return result

# Function to update the plot based on the slider value
def update(val):
    k = int(slider.val)
    y_values = [expected_OPT(n, k) for n in x_values]
    line.set_ydata(y_values)
    fig.canvas.draw_idle()

# Initial plot
x_values = np.arange(7, 61)
initial_k = 1
y_values = [expected_OPT(n, initial_k) for n in x_values]

fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.25)
line, = plt.plot(x_values, y_values, marker='o', linestyle='-', color='b')
plt.xlabel('n (Number of nodes)')
plt.ylabel('expected_OPT')
plt.title('expected_OPT vs Number of Nodes')
plt.grid(True)

# Add a slider for k
ax_slider = plt.axes([0.25, 0.1, 0.65, 0.03], facecolor='lightgoldenrodyellow')
slider = Slider(ax_slider, 'k', valmin=1, valmax=7, valinit=initial_k, valstep=1)
slider.on_changed(update)

plt.show()