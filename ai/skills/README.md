# ai/skills

Skill definitions live in per-skill folders.

Recommended layout:

- `ai/skills/<skill-name>/SKILL.md`
- `ai/skills/<skill-name>/assets/`
- `ai/skills/<skill-name>/scripts/`

Project-specific skill groups may use:

- `ai/skills/<project>/<skill-name>/SKILL.md`
- `ai/skills/<project>/<skill-name>/agents/openai.yaml`

Use grouped folders when the skills are expected to move together with a project documentation packet.

## Runtime Dependencies

Repository-local skills should be usable as Markdown-only instructions by default.

Rules:
- Do not require system Python, Node.js, Rust, or other local runtimes just to read or apply a skill.
- Keep `SKILL.md` as the authoritative skill artifact.
- Use `agents/openai.yaml` only for UI metadata.
- Add scripts only when a workflow is repetitive, fragile, and explicitly worth automating.
- If a skill needs a script, document the runtime requirement in the skill and keep the Markdown workflow useful without the script.
- For Ascent Rivals Unreal work, prefer existing Unreal Editor, Unreal MCP, C++, Blueprint, commandlet, or project tooling paths over extra developer-machine dependencies.
