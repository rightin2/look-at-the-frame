"""Draw the README test charts in light and dark versions from evals/results.json.

Same palette, fonts and layout as the shape-rotate repo's charts.
Usage: uv run --with matplotlib python assets/charts/make_charts.py
"""
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
R = json.loads((ROOT / "evals" / "results.json").read_text())

# Palette validated with the dataviz validator against GitHub's light and dark surfaces (shared with shape-rotate).
THEMES = {
    "light": dict(bg="#ffffff", text="#1f2328", muted="#59636e", grid="#d1d9e0",
                  skill="#2a78d6", plain="#eb6834", other="#c8d0d8"),
    "dark": dict(bg="#0d1117", text="#e6edf3", muted="#9198a1", grid="#30363d",
                 skill="#3987e5", plain="#d95926", other="#3d444d"),
}

for f in ("/System/Library/Fonts/HelveticaNeue.ttc", "/System/Library/Fonts/Helvetica.ttc"):
    if Path(f).exists():
        font_manager.fontManager.addfont(f)
plt.rcParams["font.family"] = ["Helvetica Neue", "Helvetica", "DejaVu Sans"]

SETUPS = [("frame", "Look at the Frame", "skill"), ("shape", "Shape Rotate", "other"),
          ("combined", "Both combined", "other"), ("baseline", "No skill", "plain")]
TASKS = [("essay", "Essay with no spine"), ("decision", "Decision going in circles"),
         ("bug", "Bug that keeps coming back")]


def score(task, setup):
    return R["tasks"][task]["scores"][setup]["score"]


def average(setup):
    return sum(score(t, setup) for t, _ in TASKS) / len(TASKS)


def label_box(t):
    """Solid background so grid lines never run through a label."""
    return dict(facecolor=t["bg"], edgecolor="none", pad=1.5)


def style(ax, t):
    ax.set_facecolor(t["bg"])
    for s in ax.spines.values():
        s.set_visible(False)
    ax.tick_params(colors=t["muted"], length=0, labelsize=10)
    ax.grid(axis="x", color=t["grid"], linewidth=0.8)
    ax.set_axisbelow(True)


def header(fig, t, title, subtitle, legend):
    fig.text(0.035, 0.94, title, fontsize=17, fontweight="bold", color=t["text"], va="top")
    fig.text(0.035, 0.865, subtitle, fontsize=11, color=t["muted"], va="top")
    x = 0.035
    fig.canvas.draw()
    for label, key in legend:
        fig.text(x, 0.79, "■", color=t[key], fontsize=13, va="center")
        txt = fig.text(x + 0.02, 0.79, label, fontsize=10.5, color=t["text"], va="center")
        bb = txt.get_window_extent(renderer=fig.canvas.get_renderer())
        x = fig.transFigure.inverted().transform((bb.x1, 0))[0] + 0.03


def chart_average(t, name):
    base = average("baseline")
    fig = plt.figure(figsize=(10, 4.8), facecolor=t["bg"])
    header(fig, t, "25% higher score with the skill",
           "Opus 5.5 answers to 3 stuck tasks, scored out of 10 by a blind Opus judge. Average of the 3 tasks.",
           legend=(("With Look at the Frame", "skill"), ("Other skills", "other"), ("No skill", "plain")))
    ax = fig.add_axes([0.2, 0.08, 0.72, 0.62])
    style(ax, t)
    for i, (key, label, colour) in enumerate(SETUPS):
        y = len(SETUPS) - 1 - i
        v = average(key)
        ax.barh(y, v, height=0.62, color=t[colour])
        note = "" if key == "baseline" else f"   +{(v / base - 1) * 100:.0f}% vs no skill"
        ax.text(v + 0.12, y, f"{v:.1f}", va="center", fontsize=12, fontweight="bold", color=t["text"], bbox=label_box(t))
        if note:
            ax.text(v + 0.55, y, note, va="center", fontsize=10, color=t["muted"], bbox=label_box(t))
        ax.text(-0.25, y, label, va="center", ha="right", fontsize=12,
                fontweight="bold" if key == "frame" else "normal", color=t["text"])
    ax.set_xlim(0, 10)
    ax.set_xticks(range(0, 11, 2))
    ax.set_yticks([])
    ax.set_ylim(-0.6, len(SETUPS) - 0.4)
    fig.savefig(OUT / f"{name}-{t['mode']}.png", dpi=200, facecolor=t["bg"])
    plt.close(fig)


def chart_tasks(t, name):
    fig = plt.figure(figsize=(10, 4.8), facecolor=t["bg"])
    header(fig, t, "Where it helps most",
           "The same Opus 5.5 with and without the skill, one run per task, scored out of 10 by a blind judge.",
           legend=(("With Look at the Frame", "skill"), ("No skill", "plain")))
    ax = fig.add_axes([0.28, 0.08, 0.64, 0.62])
    style(ax, t)
    for i, (task, label) in enumerate(TASKS):
        y = len(TASKS) - 1 - i
        b, s = score(task, "baseline"), score(task, "frame")
        ax.plot([b, s], [y, y], color=t["grid"], linewidth=6, solid_capstyle="round", zorder=1)
        ax.scatter([b], [y], s=260, color=t["plain"], zorder=2, edgecolor=t["bg"], linewidth=2)
        ax.scatter([s], [y], s=260, color=t["skill"], zorder=3, edgecolor=t["bg"], linewidth=2)
        ax.text(b - 0.22, y, str(b), va="center", ha="right", fontsize=11.5, fontweight="bold", color=t["text"], bbox=label_box(t))
        ax.text(s + 0.22, y, f"{s}", va="center", ha="left", fontsize=11.5, fontweight="bold", color=t["text"], bbox=label_box(t))
        pct = (s / b - 1) * 100
        p = f"{pct:.1f}" if f"{pct:.1f}".endswith(".5") else f"{pct:.0f}"   # 12.5% stays exact, 33.3% shows as 33%
        ax.text(s + 0.62, y, f"+{p}%", va="center", ha="left",
                fontsize=10.5, color=t["muted"], bbox=label_box(t))
        ax.text(4.3, y, label, va="center", ha="right", fontsize=12, color=t["text"])
    ax.set_xlim(4.6, 10)
    ax.set_xticks(range(5, 11))
    ax.set_yticks([])
    ax.set_ylim(-0.6, len(TASKS) - 0.4)
    fig.savefig(OUT / f"{name}-{t['mode']}.png", dpi=200, facecolor=t["bg"])
    plt.close(fig)


if __name__ == "__main__":
    for mode, t in THEMES.items():
        t["mode"] = mode
        chart_average(t, "average")
        chart_tasks(t, "by-task")
    print(sorted(p.name for p in OUT.glob("*.png")))
