"""Plot only the exact outward coefficient bounds in the finite certificate."""
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

out = Path(__file__).resolve().parent.parent / "figures"
ranks = [160080, 160320, 160560]
lower = [1556, 1482, 1565]
upper = [1615, 1541, 1624]
colours = ["#64456E", "#BA6B3B", "#64456E"]
plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 10,
    "axes.spines.top": False, "axes.spines.right": False
})
fig, ax = plt.subplots(figsize=(6.6, 3.25), constrained_layout=True)
for x, lo, hi, colour in zip(ranks, lower, upper, colours):
    ax.plot([x, x], [lo, hi], color=colour, linewidth=5, solid_capstyle="butt")
    ax.plot([x-18, x+18], [lo, lo], color=colour, linewidth=2)
    ax.plot([x-18, x+18], [hi, hi], color=colour, linewidth=2)
    ax.text(x+28, lo, str(lo), va="center", fontsize=9, color=colour)
    ax.text(x+28, hi, str(hi), va="center", fontsize=9, color=colour)
ax.axhspan(1541, 1556, color="#A9B9A0", alpha=.28, zorder=0)
ax.axhline(1541, color="#BA6B3B", linewidth=.8, linestyle=(0,(4,4)), alpha=.65)
ax.set_xlim(159980, 160685)
ax.set_ylim(1460, 1645)
ax.set_xticks(ranks)
ax.xaxis.set_major_formatter(FuncFormatter(lambda x, pos: f"{int(x):,}"))
ax.set_xlabel("Dominating-set size k")
ax.set_ylabel(r"Certified bounds for $10^6d_k/2^{314880}$")
ax.text(.01, .96, "Both connected examples have 317,440 vertices",
        transform=ax.transAxes, va="top", fontsize=10)
ax.grid(axis="y", alpha=.14)
fig.savefig(out/"coefficient-bounds.pdf")
fig.savefig(out/"coefficient-bounds.png", dpi=220)
