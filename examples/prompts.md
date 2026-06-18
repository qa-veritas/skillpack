# Example prompts

How an agent uses skillpack to stay cheap on context.

## Route a task to the right skills

> A task came in: "the data mount is filling up, will it run out
> tonight?" Run `skillpack match` on it, load only the top-ranked
> skill's full instructions, and follow them. Don't load skills the
> task didn't match.

## Compose matched skills

> For "the cluster is degraded and a node's disk is full," more than one
> skill matches. Load `analyze_cluster_health` and `check_disk_pressure`,
> run the health verdict first, then the disk verdict on the flagged
> node, and combine them into one finding.

## Author a new skill

> Add a skill `detect_resource_leak`. Create
> `skills/detect_resource_leak/SKILL.md` with frontmatter (name,
> description, tags), purpose/inputs/outputs/prompt-template/examples,
> register it in `registry.yaml`, and run `skillpack validate`.

## Verify prerequisites before relying on a skill

> Before using `check_disk_pressure` in an automated run, run
> `skillpack smoke check_disk_pressure` to confirm its prerequisites
> work. If it reports "skipped," the skill ships no smoke check — note
> that.
