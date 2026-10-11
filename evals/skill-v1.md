---
name: look-at-the-frame
description: Use when two fixes or drafts have failed, when a list of cases keeps growing without converging, when evidence needs special pleading to fit, when a detail fits no category, or when a choice seems stuck between two opposite options.
---

# Look at the Frame

## What it changes
In repeated-fix loops and stuck either/or choices, Claude stops producing variants of the same answer once failures reach a set count. Instead it changes an assumption every attempt shared. It refuses to swing to the opposite of its last attempt, because a reversal keeps the same frame.

## Steps
1. Trigger on a count or a visible signal, not a feeling. Fire when any of these happens:
   - two fixes or drafts have failed
   - a list of cases keeps growing without converging
   - the working hypothesis needs special pleading to fit evidence or feedback
   - a detail fits no category in play
   - the user brings an either/or choice, or says they keep going back and forth

   Below the trigger, keep iterating locally. When it fires, say "Reframing" and stop editing the answer.
2. List the constraints you have been assuming. For a user's binary, list the assumptions both options share (who the buyer is, what counts as success, that one must be chosen). Mark each one as imposed (stated by the user, the data or the code) or projected (added by you or carried in the question). Keep the labels visible in the reply. An implied judgment does not count. Check the list against what the attempts actually did, not what you meant them to do.
3. Name what all failed attempts held constant. Change one shared element on the next attempt, preferably a projected one, and tell the user which one so they can judge the attempt. The new attempt should differ in kind. A new arrangement of the same parts is not a change.
4. Check whether the planned attempt is just the opposite of the last one, such as stricter versus looser, shorter versus longer, or one big block versus many small ones. For any binary, yours or the user's:
   - name the presupposition both poles share
   - test it against what the user or data actually stated, before scoring the poles against each other
   - look for an option that is neither pole. A blend or midpoint of both poles is still inside the frame.

   If the user demands a pick, give one clearly, but only after this test. The pick may be the third option.
5. Reframe with one move, then check it against the real problem. Options:
   - Zoom out a level: function, module, project, user goal.
   - Look for an invariant or constraint already visible that would make the answer follow directly.
   - Map to a distant analogy. Say which features carry over and which do not. Reject analogies too close to add anything or too loose to name a shared structure.
   - Restate the problem in the third person. Keep it only if different features stand out.

   Stop exploring when new framings look no different from the current one.
6. If the reframe works but needs material you lack, still deliver a concrete attempt in the new frame, such as a short sample with invented details clearly marked, then ask for the material. If several shared elements could be the culprit and only the user's facts can decide between them, make the attempt conditional. Ask the direct question and say which answer points to which fix, rather than committing fully to one and listing the others as caveats. If the answer rests on facts you recall rather than can verify, mark inline which claims are firm and which are uncertain or your own inference. One closing disclaimer does not count. Name the exact sources that would settle it, and ask for the user's conflicting sources. If no reframe works, stop. Name the missing premise, data or constraint, say why more reasoning on current information will not supply it, and ask for it.
7. When finalising, name the frame you adopted in plain terms, and the specific things it cannot see. Check the conclusion against each one and keep them as live constraints in the answer. No generic caveat.

## Where the idea comes from
In the nine-dot puzzle, Vervaeke shows that people fail because they project a square onto the dots, not because of anything in the data. Kaplan and Simon's heuristic follows: when attempts keep failing, ask what you keep not changing.

Siddhartha swung from indulgence to self-denial and both failed: "When you negate something you are still framing it in the same way."

The mutilated chessboard shows insight as swapping an explosive formulation (trying coverings) for one that collapses the search (parity).

Vervaeke also rejects presuppositions shared by both sides of a debate, looks for a third relation inside forced binaries, and uses zooming out, third person restatement and apt analogy to break frame. Special pleading and stray anomalies signal a failing schema. Breaking and making frame must be balanced. The framing process never shows up inside the frame, and naming a limit only in passing is a way of forgetting it.

## Where it may not transfer
A conversation keeps conditioning on its first framing, and failed attempts are visible in the transcript, so they can be counted.

Felt impasse, anxiety narrowing and incubation have no clear model counterpart, which is why the trigger is a count or a visible signal. For a model, third person restatement is a paraphrase, useful only if it changes what is salient.

The list of shared assumptions is Claude's own reading and can be wrong, hence the check in step 2. Reframing can also fire too early and drop an approach that needed one more local fix. The count guards against that as well as against endless iteration.