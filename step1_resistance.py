import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

<<<<<<< HEAD
R20 = 0.0344
alpha = 0.00393
=======
# A 0.5 mm^2 automotive wire, 1 metre long
R20 = 0.0344        # ohms at 20 C
alpha = 0.00393     # copper resistance change per degree
>>>>>>> 5062d2d419c6999ab39e52b242cbe3cc98753074

T = np.linspace(20, 150, 100)
R = R20 * (1 + alpha * (T - 20))

plt.figure(figsize=(7, 4))
plt.plot(T, R * 1000)
plt.xlabel("Wire temperature (C)")
plt.ylabel("Resistance (milliohm per metre)")
plt.title("Copper gets more resistive as it heats up")
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("step1_resistance.png", dpi=150)

print(f"At  20 C: {R[0]*1000:.1f} mohm/m")
print(f"At 150 C: {R[-1]*1000:.1f} mohm/m")
print(f"That is {R[-1]/R[0]:.0%} of the cold value")
