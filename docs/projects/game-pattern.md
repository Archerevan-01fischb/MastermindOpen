# Game Project Pattern

Canonical shape for a multi-platform game project.

## Engine choice

The right engine depends on the game:

| Engine | Strengths | Weaknesses |
|---|---|---|
| **Bevy** (Rust) | Memory safety, ECS-native, no royalties, fast compile-incremental | Smaller asset toolchain ecosystem, young (breaking API changes between versions) |
| **Unreal** (C++ / Blueprints) | AAA-grade rendering, mature toolchain, huge marketplace | Royalties past $1M, heavy, opinionated |
| **Unity** (C#) | Middle-ground, huge tutorial / asset ecosystem | Pricing changes (history of policy reversals), C# garbage collection nuances |
| **Godot** (GDScript / C# / Rust) | Open-source, no royalties, lightweight | Smaller industry adoption, less mature 3D rendering |

Pick once and commit. The cost of switching engines mid-project is enormous. If the game is small and you're learning, start with the engine you're most comfortable with.

## Asset pipeline

Source assets → exported assets → engine import. Each step has a tool:

```
Source (Maya / Blender / Photoshop / Audition)
   ↓ export
Standard format (FBX / glTF / PNG / OGG)
   ↓ engine import
Engine-native format (uasset / scene / etc.)
```

**Conventions that pay off:**

- Source assets in a separate dir from the repo (too big to commit). Reference by path.
- Exported assets in `assets/` committed.
- Naming convention: stick to one. Examples:
  - `pascal_case_directories/PascalCaseFiles.ext`
  - `snake_case_directories/snake_case_files.ext`
- One-line export protocol per asset type, documented in CLAUDE.md ("PNG: sRGB, no alpha unless needed, power-of-2 dimensions").

## Multi-platform build

### Common approach: GitHub Actions on tag push

```yaml
# .github/workflows/release.yml
on:
  push:
    tags:
      - 'v*'
jobs:
  build-windows: ...
  build-mac: ...
  build-linux: ...
  upload-to-releases: ...
```

Trigger: `git tag v0.1.0 && git push --tags`. CI builds for all platforms, uploads to GitHub Releases or your distribution target.

### Distribution targets

- **Steam** — `steamcmd` upload, mature pipeline, takes 30%.
- **itch.io** — friendly, no upfront cost, lower visibility.
- **GOG** — manual upload via partner portal.
- **Self-hosted downloads** — your own domain serves binaries (need TLS + Cloudflare in front for bandwidth).

If you self-host: keep binaries in object storage (R2, S3, B2) and serve from there. Don't put them in the same VPS as your website.

## Multi-platform gotchas

- **macOS code signing + notarization:** required for users to open without warnings. Apple Developer account is $99/yr. Don't skip — your audience will tell you "the game won't open" and bounce.
- **Windows code signing:** users now get SmartScreen warnings if not signed. Sigstore-style free signing options exist but are immature; cheapest paid certs are ~$100/yr.
- **Linux:** Steam Runtime + Proton handle most of this; for native Linux builds outside Steam, AppImage is the easiest distribution format.

## Save game files

Where to put them per platform (use library or framework helpers — don't hard-code):

- Windows: `%APPDATA%/{GameName}/saves/`
- macOS: `~/Library/Application Support/{GameName}/saves/`
- Linux: `~/.local/share/{game_name}/saves/`

## Release checklist

Before tagging:

- [ ] Version bumped in the appropriate `Cargo.toml` / `pubspec.yaml` / `.uproject`.
- [ ] CHANGELOG updated.
- [ ] All tests passing locally.
- [ ] Smoke-tested on at least 2 platforms.
- [ ] Asset licenses audited (no copyrighted music / textures).
- [ ] Save-game compatibility verified (or breaking-save changelog entry written).
- [ ] Screenshots / press kit updated if marketing material is changing.

## Debug guidelines

Document game-specific debug commands in CLAUDE.md:

- **Engine logs:** where they go on each platform.
- **Console commands:** what flags exist (`--debug`, `--skip-intro`, etc.).
- **Profile flag:** how to run with profiler attached.
- **Telemetry:** if you have it, what's collected and where it goes.

## When this earns a child Claude

Multi-month or multi-year game projects often earn a dedicated child (the "Frostsmith" pattern — see [child-mastermind-pattern.md](child-mastermind-pattern.md)). The child becomes the project-lead Claude with its own identity, accumulates project-specific lore (game balance, asset conventions, debugging history), and is the only Claude you talk to in that project window.

## Read also

- `templates/project-types/game/CLAUDE.md.template` — bootstrap template
- [child-mastermind-pattern.md](child-mastermind-pattern.md) — when to spawn a dedicated Claude
- [spec-driven-pattern.md](spec-driven-pattern.md) — useful for reverse-engineering existing games / remasters
