import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

R20, alpha = 0.0344, 0.00393
Cth, Rth   = 2.5, 9.0
T_limit    = 105.0
T_TRIP     = 95.0     # trip early, leave safety margin

def time_to_limit(current, T_amb, max_time=600.0, dt=0.001):
    T = T_amb
    for i in range(int(max_time / dt)):
        R = R20 * (1 + alpha * (T - 20))
        T += (current**2 * R - (T - T_amb) / Rth) / Cth * dt
        if T >= T_limit:
            return i * dt
    return None

def thermal_model_trip(current, T_amb, max_time=600.0, dt=0.001):
    """The eFuse runs its own copy of the cable model and trips on
       ESTIMATED temperature, not on accumulated I^2*t."""
    T_est = T_amb
    for i in range(int(max_time / dt)):
        R = R20 * (1 + alpha * (T_est - 20))
        T_est += (current**2 * R - (T_est - T_amb) / Rth) / Cth * dt
        if T_est >= T_TRIP:
            return i * dt
    return None

def i2t_trip_time(current, K):
    return K / current**2

K = 30**2 * time_to_limit(30, 25.0)
currents = np.arange(15, 61, 1.0)

plt.figure(figsize=(8, 6))
for T_amb, c in [(25, "tab:blue"), (85, "tab:red")]:
    dmg = [(I, time_to_limit(I, T_amb)) for I in currents]
    dmg = [(I, t) for I, t in dmg if t]
    plt.loglog([p[0] for p in dmg], [p[1] for p in dmg], color=c, lw=2,
               label=f"cable damage, {T_amb} C")

    trip = [(I, thermal_model_trip(I, T_amb)) for I in currents]
    trip = [(I, t) for I, t in trip if t]
    plt.loglog([p[0] for p in trip], [p[1] for p in trip], color=c,
               lw=1.8, linestyle=":", label=f"thermal model trips, {T_amb} C")

plt.loglog(currents, [i2t_trip_time(I, K) for I in currents],
           "k--", lw=2, label="fixed I2t (old method)")

plt.xlabel("Current (A)")
plt.ylabel("Time (s)")
plt.title("Thermal-model eFuse adapts to ambient; fixed I2t does not")
plt.legend(fontsize=8)
plt.grid(True, which="both", alpha=0.3)
plt.tight_layout()
plt.savefig("step5_thermal_model.png", dpi=150)

print(f"{'I':>4} {'amb':>5} {'damage':>8} {'I2t':>8} {'model':>8}   I2t      model")
for T_amb in [25, 85]:
    for I in [20, 30, 40, 50]:
        d  = time_to_limit(I, T_amb)
        f  = i2t_trip_time(I, K)
        m  = thermal_model_trip(I, T_amb)
        v1 = "DAMAGED" if f > d else "ok"
        v2 = "DAMAGED" if m > d else "ok"
        print(f"{I:4.0f} {T_amb:5.0f} {d:8.2f} {f:8.2f} {m:8.2f}   {v1:8} {v2}")