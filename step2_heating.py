import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# --- wire properties (0.5 mm^2 automotive cable, 1 m) ---
R20   = 0.0344     # ohm, resistance at 20 C
alpha = 0.00393    # copper temperature coefficient
Cth   = 2.5        # J/K   heat needed to raise wire 1 degree
Rth   = 9.0        # K/W   how badly heat escapes to air

T_amb = 25.0       # ambient air temperature, C
T_limit = 105.0    # PVC insulation melts above this

# --- simulate 60 seconds at three different currents ---
dt = 0.001
t = np.arange(0, 60, dt)

plt.figure(figsize=(8, 5))

for current in [10, 15, 25]:
    T = T_amb
    history = []
    for _ in t:
        R = R20 * (1 + alpha * (T - 20))   # resistance right now
        heat_in  = current**2 * R          # watts generated
        heat_out = (T - T_amb) / Rth       # watts escaping
        T = T + (heat_in - heat_out) / Cth * dt
        history.append(T)
    plt.plot(t, history, label=f"{current} A")

plt.axhline(T_limit, color="red", linestyle="--", label="insulation limit")
plt.xlabel("Time (seconds)")
plt.ylabel("Wire temperature (C)")
plt.title("How a 0.5 mm2 wire heats up")
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("step2_heating.png", dpi=150)
print("saved step2_heating.png")