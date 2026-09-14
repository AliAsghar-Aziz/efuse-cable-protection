import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

R20 = 0.0344
alpha = 0.00393

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
