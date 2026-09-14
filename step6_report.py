import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

R20, alpha = 0.0344, 0.00393
Cth, Rth   = 2.5, 9.0
T_limit, T_TRIP = 105.0, 95.0

def simulate(current, T_amb, limit, max_time=600.0, dt=0.001):
    T = T_amb
    for i in range(int(max_time / dt)):
        R = R20 * (1 + alpha * (T - 20))
        T += (current**2 * R - (T - T_amb) / Rth) / Cth * dt
        if T >= limit:
            return i * dt
    return None

damage = lambda I, Ta: simulate(I, Ta, T_limit)
model  = lambda I, Ta: simulate(I, Ta, T_TRIP)
K      = 30**2 * damage(30, 25.0)
i2t    = lambda I: K / I**2

ambients = [-20, 25, 60, 85, 100]
currents = [20, 30, 40, 50]

rows = []
for Ta in ambients:
    for I in currents:
        d, m, f = damage(I, Ta), model(I, Ta), i2t(I)
        if d is None or d <= 0:
            continue   # ambient at/above the insulation limit: no current is safe
        rows.append(dict(amb=Ta, I=I, damage=d, i2t=f, model=m,
                         i2t_margin=(d - f) / d * 100,
                         model_margin=(d - m) / d * 100))

print(f"{'amb':>5}{'I':>5}{'damage':>9}{'I2t':>8}{'model':>8}"
      f"{'I2t marg':>10}{'mdl marg':>10}")
for r in rows:
    print(f"{r['amb']:5.0f}{r['I']:5.0f}{r['damage']:9.2f}{r['i2t']:8.2f}"
          f"{r['model']:8.2f}{r['i2t_margin']:9.0f}%{r['model_margin']:9.0f}%")

fails_i2t   = sum(1 for r in rows if r['i2t_margin']   < 0)
fails_model = sum(1 for r in rows if r['model_margin'] < 0)
print(f"\nFixed I2t   fails {fails_i2t}/{len(rows)} conditions")
print(f"Thermal model fails {fails_model}/{len(rows)} conditions")

with open("results.csv", "w") as f:
    f.write("ambient_C,current_A,damage_s,i2t_trip_s,model_trip_s,"
            "i2t_margin_pct,model_margin_pct\n")
    for r in rows:
        f.write(f"{r['amb']},{r['I']},{r['damage']:.4f},{r['i2t']:.4f},"
                f"{r['model']:.4f},{r['i2t_margin']:.1f},{r['model_margin']:.1f}\n")

fig, ax = plt.subplots(1, 2, figsize=(13, 5.5))
Isweep = np.arange(15, 61, 1.0)
for Ta in ambients:
    d = [(I, damage(I, Ta)) for I in Isweep]
    d = [(I, t) for I, t in d if t]
    ax[0].loglog([p[0] for p in d], [p[1] for p in d], lw=1.8, label=f"{Ta} C")
ax[0].loglog(Isweep, [i2t(I) for I in Isweep], "k--", lw=2.2, label="fixed I2t")
ax[0].set_title("Fixed I2t cannot follow ambient")
ax[0].legend(fontsize=8, title="ambient")

for Ta in ambients:
    d = [(I, damage(I, Ta)) for I in Isweep]; d = [(I,t) for I,t in d if t]
    m = [(I, model(I, Ta))  for I in Isweep]; m = [(I,t) for I,t in m if t]
    ln, = ax[1].loglog([p[0] for p in d], [p[1] for p in d], lw=1.8, label=f"{Ta} C")
    ax[1].loglog([p[0] for p in m], [p[1] for p in m], ":",
                 lw=1.8, color=ln.get_color())
ax[1].set_title("Thermal model tracks every ambient (dotted = trip)")
ax[1].legend(fontsize=8, title="ambient")

for a in ax:
    a.set_xlabel("Current (A)")
    a.set_ylabel("Time (s)")
    a.grid(True, which="both", alpha=0.3)

plt.tight_layout()
plt.savefig("step6_comparison.png", dpi=150)
print("\nsaved step6_comparison.png and results.csv")