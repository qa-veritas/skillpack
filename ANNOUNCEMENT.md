# LinkedIn announcement — skillpack

If you give an agent every capability it might ever need in one system
prompt, it gets worse at all of them. Context is a budget. Spend it on
the task in front of you, not the 30 tasks that aren't.

`skillpack` is a tiny framework for progressive-disclosure skills:

- **Level 1** — name + description, always loaded, ~100 tokens per
  skill. This is all the agent sees at rest.
- **Level 2** — the full `SKILL.md` instructions, loaded *only* when a
  task matches the description.
- **Level 3** — `scripts/` and `kb/` resources, loaded only when the
  skill references them, and run via the shell so they never enter the
  context window at all.

A skill carries *knowledge, not a command list*: what a signal means,
what inputs to expect, what a good answer looks like — then it lets the
agent reason. Matching is deliberately transparent (token overlap over
name + description + tags); the point isn't a clever ranker, it's that
the agent only pays for the skills a task actually needs.

There's a smoke-check convention too: a cheap, read-only command that
proves a skill's prerequisites work before an automated run relies on
it.

It's ~300 lines of Python and a directory convention. The discipline is
worth more than the code: self-contained, composable, filesystem-based
skills you can review like any other artifact.

Repo: github.com/qa-veritas/skillpack

#aiengineering #agents #platformengineering #llm

MIT licensed.
