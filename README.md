<p align="center">
  <img src="assets/poster.png" alt="A dark square with the words 'Three fixes. Still broken.' over three small cards, each one a failed attempt." width="100%">
</p>

<h1 align="center">Look at the Frame</h1>

<p align="center"><b>A Claude skill for when attempts keep failing.</b><br>
It finds the assumption every attempt shares, and changes that instead of trying a fourth variation.</p>

<p align="center">
  <img src="https://img.shields.io/badge/Claude-skill-E8735A" alt="Claude skill">
  <img src="https://img.shields.io/badge/Claude%20Code-plugin-3E8E8A" alt="Claude Code plugin">
  <img src="https://img.shields.io/badge/license-MIT-5B6C8F" alt="MIT license">
</p>

---

You have fixed it twice. Then three times. Each fix clears one test and breaks another.

Usually the fix is not wrong. Every attempt was built on the same unexamined assumption, so every attempt was a variation on one mistake. This skill makes Claude count the failed attempts, name what they all took for granted, and change that one thing.

[Watch the 15 second video](assets/look-at-the-frame.mp4)

## Install

**Claude Code (recommended):**

```bash
/plugin marketplace add rightin2/look-at-the-frame
/plugin install look-at-the-frame@look-at-the-frame
```

<details>
<summary><b>Manual install</b></summary>

Clone the repo and copy the skill folder into your skills directory:

```bash
git clone https://github.com/rightin2/look-at-the-frame.git
cp -r look-at-the-frame/skills/look-at-the-frame ~/.claude/skills/
```

</details>

Update later with `claude plugin update look-at-the-frame@look-at-the-frame`.

## Try it

Ask in plain words once the attempts have started to fail:

- "My script assigns bookings to the wrong week near midnight. I have tried three fixes and each breaks another test. Look at the frame."
- "I have rewritten this discussion section three times and it still feels flat. What am I assuming about the reader?"

The skill runs on its own when you describe repeated failure, a list of special cases that keeps growing, or a choice stuck between two opposite options.

## What it does

- **Counts the failures.** It lists each attempt and what it changed.
- **Names the shared assumption.** Whatever every attempt held constant is the frame.
- **Labels each assumption.** Is it a real constraint, or something projected onto the problem?
- **Changes the frame, not the answer.** It tries an attempt that differs in kind, and states the frame it adopted and what that frame cannot see.

## Does it work?

In a small blind test, Opus judged answers to three realistic tasks: a bug that keeps returning, an essay with no spine, and a decision that keeps going round in circles. Answers with this skill averaged **8.3 out of 10**. Answers with no skill averaged **6.7**.

It is three tasks, run once each, so treat it as a first signal, not proof. The raw scores and the judge's reasons are in [`evals/results.json`](evals/results.json).

## What's inside

```
skills/look-at-the-frame/SKILL.md   the skill itself
.claude-plugin/                     plugin and marketplace manifests
evals/results.json                  the blind test scores and judge reasons
assets/                             poster and video
```

## Limits

- It works best when you can count the failed attempts. If nothing has failed yet, it has nothing to find.
- It names an assumption, but it cannot check that the assumption is true. You still have to test it.
- The evidence is one small test, scored by a model, not by people.

## Origin

Built from ideas in John Vervaeke's *Awakening from the Meaning Crisis* lecture series, on how a mind builds the frame it sees a problem through.

## Licence

MIT. See [LICENSE](LICENSE).
