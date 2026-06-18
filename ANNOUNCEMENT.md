# LinkedIn announcement — SkillPack

---

The instinct when giving an agent capability is to stuff every instruction it might need into one system prompt. That makes it worse at all of them. Context is a budget, and a prompt bloated with thirty procedures spends it on the twenty-nine that don't matter for the task in front of it. Capability that doesn't scale with the number of skills isn't capability — it's a ceiling.

SkillPack loads capability progressively, in three levels: ~100 tokens of metadata always available, the full instructions only when a task matches, and scripts or reference material only when the skill actually reaches for them. A skill carries *knowledge* — what to look at and what each signal means — not a fixed command list. The agent reasons; the skill informs. (A skill that hands a fixed command list is a script in costume.)

The hundredth skill you add doesn't degrade the first ninety-nine, because nothing loads until a task invokes it.

This is the **Skills** layer of QA Veritas — a platform exploring how AI agents reason about, verify, and operate complex systems. It's the connective tissue: the triage, verification, and diagnostic knowledge an agent applies, packaged as capability it loads on demand.

Repo + write-up in the comments.

---
*First comment:* Repo: github.com/qa-veritas/skillpack · Platform: github.com/qa-veritas
