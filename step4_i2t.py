import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

R20, alpha = 0.0344, 0.00393
Cth, Rth   = 2.5, 9.0
T_limit    = 105.0

def time_to_limit(current, T_amb, max_time=600.0, dt=0.001):
    T = T_amb
    for i in range(int(max_time / dt)):
        R = R20 * (1 + alpha * (T - 20))
        T += (current**2 * R - (T - T_amb) / Rth) / Cth * dt
        if T >= T_limit:
            return i * dt
    return None

def i2t_trip_time(current, threshold):
    """Simple I^2*t fuse: trips when current^2 * time reaches threshold."""
    return threshold / current**2

# Tune the I2t threshold so it JUST protects at 25 C and 30 A
K = 30**2 * time_to_limit(30, 25.0)
print(f"I2t threshold set to {K:.0f} A^2*s\n")

currents = np.arange(15, 61, 1.0)

plt.figure(figsize=(8, 6))
for T_amb, colour in [(25, "tab:blue"), (85, "tab:red")]:
    cable = [(I, time_to_limit(I, T_amb)) for I in currents]
    cable = [(I, t) for I, t in cable if t is not None]
    plt.loglog([p[0] for p in cable], [p[1] for p in cable],
               color=colour, lw=2, label=f"cable damage, ambient {T_amb} C")

plt.loglog(currents, [i2t_trip_time(I, K) for I in currents],
           "k--", lw=2, label="I2t fuse trips here")

plt.xlabel("Current (A)")
plt.ylabel("Time (s)")
plt.title("Fixed I2t protection vs real cable limits")
plt.legend()
plt.grid(True, which="both", alpha=0.3)
plt.tight_layout()
plt.savefig("step4_i2t.png", dpi=150)

print(f"{'I':>5} {'fuse':>9} {'25C':>9} {'85C':>9}   verdict at 85 C")
for I in [18, 20, 25, 30, 40, 50]:
    tf = i2t_trip_time(I, K)
    t25 = time_to_limit(I, 25.0)
    t85 = time_to_limit(I, 85.0)
    v = "CABLE DAMAGED" if (t85 and tf > t85) else "ok"
    print(f"{I:5.0f} {tf:9.2f} {t25:9.2f} {t85 if t85 else 0:9.2f}   {v}")