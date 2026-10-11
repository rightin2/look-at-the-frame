"""Draw the README test charts in light and dark versions from evals/v2-test/results.json.

Same palette, fonts and layout as the shape-rotate repo's charts. The same file is used in the
look-at-the-frame and heat-then-cool repos; it picks the skill from the repo folder name.
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
R = json.loads((ROOT / "evals" / "v2-test" / "results.json").read_text())
SKILL = {"look-at-the-frame": ("frame", "Look at the Frame"),
         "heat-then-cool": ("anneal", "Heat Then Cool")}[ROOT.name]
KEY, NAME = SKILL

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

TASK_NAMES = {
    "launchd-backup-script-fails": "Backup script fails when scheduled",
    "react-list-scroll-reset": "App list keeps jumping to the top",
    "burnout-article-wont-flow": "Article the editor says won't flow",
    "monday-no-shows": "Monday no-shows",
    "sumifs-reconciliation-gap": "Spreadsheet that won't reconcile",
    "gp-referral-outreach-flat": "GP outreach getting no referrals",
    "same-day-notes-backlog": "Same-day notes backlog",
    "duplicate-work-with-collaborator": "Duplicated work with a collaborator",
}


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


def chart_stuck(t, name):
    c = R["conditions"]
    rows = [(f"{KEY}2", f"{NAME} v2", "skill"), (f"{KEY}1", f"{NAME} v1", "other"), ("baseline", "No skill", "plain")]
    pct = c[f"{KEY}2"]["pct_vs_baseline_stuck"]
    fig = plt.figure(figsize=(10, 4.4), facecolor=t["bg"])
    header(fig, t, f"{pct:.0f}% higher on stuck problems",
           "Opus 5.5 on 8 stuck tasks, 3 runs each. Scored out of 10 by two blind judges (Opus 5.5 and GPT-6.1 Sol).",
           legend=((f"{NAME} v2 (this repo)", "skill"), ("v1 (earlier version)", "other"), ("No skill", "plain")))
    ax = fig.add_axes([0.25, 0.08, 0.66, 0.6])
    style(ax, t)
    for i, (k, label, colour) in enumerate(rows):
        y = len(rows) - 1 - i
        v = c[k]["stuck"]
        ax.barh(y, v, height=0.6, color=t[colour])
        ax.text(v + 0.1, y, f"{v:.1f}", va="center", fontsize=12, fontweight="bold", color=t["text"], bbox=label_box(t))
        if k != "baseline":
            lo, hi = c[k]["ci95_stuck"]
            note = f"{c[k]['pct_vs_baseline_stuck']:+.0f}% vs no skill"
            note += "" if lo > 0 else " (within chance)"
            ax.text(v + 0.5, y, note, va="center", fontsize=10, color=t["muted"], bbox=label_box(t))
        ax.text(-0.25, y, label, va="center", ha="right", fontsize=12,
                fontweight="bold" if k.endswith("2") else "normal", color=t["text"])
    ax.set_xlim(0, 10)
    ax.set_xticks(range(0, 11, 2))
    ax.set_yticks([])
    ax.set_ylim(-0.6, len(rows) - 0.4)
    fig.savefig(OUT / f"{name}-{t['mode']}.png", dpi=200, facecolor=t["bg"])
    plt.close(fig)


def chart_tasks(t, name):
    per = R["per_task"]
    tasks = sorted(TASK_NAMES, key=lambda k: per[k][f"{KEY}2"] - per[k]["baseline"])
    fig = plt.figure(figsize=(10, 6.4), facecolor=t["bg"])
    header(fig, t, "Task by task",
           "Average of 3 runs and two blind judges per task. The 8 stuck tasks were written by an agent that never saw the skill.",
           legend=((f"With {NAME} v2", "skill"), ("No skill", "plain")))
    ax = fig.add_axes([0.36, 0.07, 0.56, 0.66])
    style(ax, t)
    for y, k in enumerate(tasks):
        b, s = per[k]["baseline"], per[k][f"{KEY}2"]
        ax.plot([b, s], [y, y], color=t["grid"], linewidth=6, solid_capstyle="round", zorder=1)
        ax.scatter([b], [y], s=200, color=t["plain"], zorder=2, edgecolor=t["bg"], linewidth=2)
        ax.scatter([s], [y], s=200, color=t["skill"], zorder=3, edgecolor=t["bg"], linewidth=2)
        d = s - b
        ax.text(max(b, s) + 0.18, y, f"{d:+.1f}" if abs(d) >= 0.05 else "same", va="center", fontsize=10.5,
                color=t["text"], bbox=label_box(t))
        ax.text(4.85, y, TASK_NAMES[k], va="center", ha="right", fontsize=11.5, color=t["text"])
    ax.set_xlim(5, 10)
    ax.set_xticks(range(5, 11))
    ax.set_yticks([])
    ax.set_ylim(-0.6, len(tasks) - 0.4)
    fig.savefig(OUT / f"{name}-{t['mode']}.png", dpi=200, facecolor=t["bg"])
    plt.close(fig)


if __name__ == "__main__":
    for mode, t in THEMES.items():
        t["mode"] = mode
        chart_stuck(t, "stuck-tasks")
        chart_tasks(t, "by-task")
    print(sorted(p.name for p in OUT.glob("*.png")))
