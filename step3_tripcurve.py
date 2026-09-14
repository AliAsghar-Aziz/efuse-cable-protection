import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

R20   = 0.0344
alpha = 0.00393
Cth   = 2.5
Rth   = 9.0
T_amb   = 25.0
T_limit = 105.0

def time_to_limit(current, max_time=600.0, dt=0.001):
    """How many seconds until this current overheats the wire?
       Returns None if the wire never gets there."""
    T = T_amb
    steps = int(max_time / dt)
    for i in range(steps):
        R = R20 * (1 + alpha * (T - 20))
        T += (current**2 * R - (T - T_amb) / Rth) / Cth * dt
        if T >= T_limit:
            return i * dt
    return None

currents = np.arange(8, 61, 0.5)
times, safe_currents = [], []

for I in currents:
    t = time_to_limit(I)
    if t is None:
        safe_currents.append(I)
    else:
        times.append((I, t))

I_trip = [p[0] for p in times]
t_trip = [p[1] for p in times]

plt.figure(figsize=(7.5, 5.5))
plt.loglog(I_trip, t_trip, lw=2)
plt.xlabel("Current (A)")
plt.ylabel("Time until insulation damage (s)")
plt.title("Cable trip curve: 0.5 mm2, ambient 25 C")
plt.grid(True, which="both", alpha=0.3)
plt.tight_layout()
plt.savefig("step3_tripcurve.png", dpi=150)

print(f"Safe forever below about {max(safe_currents):.1f} A")
for I in [15, 20, 30, 50]:
    t = time_to_limit(I)
    print(f"{I:3.0f} A  ->  damage after {t:6.2f} s" if t else f"{I:3.0f} A  ->  safe")