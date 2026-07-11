# Strange Times — Claude Working Instructions

## Default "Update" Process

When the user asks for an **update** (any request phrased as "run an update", "do an update", "update the site", etc.), the default workflow is:

1. **Google Drive sync** — Check `lastChecked` date in `.claude/drive-index.json`. Read any Drive docs with `modifiedTime` newer than that date. Download any new images from the Drive images folder.

2. **Apply changes** — Update `index.html` with any new content from changed docs. Add newly downloaded images to the appropriate sections.

3. **Update drive-index.json** — Set `lastChecked` to today's date. Update `modifiedTime` entries for any docs that were re-read.

4. **Commit** — Stage and commit all changes with a descriptive message.

5. **Push** — Push to `claude/index-file-review-41udxw` (or the current working branch).

6. **Merge to main** — Create a PR and merge it to main. After a successful merge, reset the branch from the latest main before any follow-up work.

## Branch Management

- Working branch: `claude/index-file-review-41udxw`
- After a PR merges to main, always restart the branch: `git fetch origin main && git checkout -B claude/index-file-review-41udxw origin/main`
- Never force-push. Use `git merge origin/main` to integrate upstream changes, resolving conflicts by taking our changes (we are always a superset).

## Drive Tools

- MCP server prefix: `mcp__1f305485-e137-4be1-9d46-f00e90d4071f__*`
- Drive index: `.claude/drive-index.json`
- Images folder ID: `1vLxDomJrI2TNngYHlIfr-6jDLxalH6bZ`
- Docs folder ID: `1aDM2JhiIZplXy1EbQBlob-Te6uJQJEHt`
- Images that return oversized base64: save the tool result to disk, then decode with `jq -r .content <file> | base64 -d > images/filename.png`

## Site Structure

- Single-page HTML: `index.html` (~3000+ lines)
- Dark parchment theme, Cinzel/EB Garamond fonts, gold accents (`#c9963a`, `var(--gold)`)
- Key CSS classes: `.read-aloud`, `.dm-note`, `.dm-note-label`, `.area-card`, `.area-header`, `.area-number` (span), `.area-body`, `.check-list`, `.dc-badge`, `.figure-card`, `.figure-name`, `.figure-subtitle`, `.figure-body`, `.session-ending`, `.session-review`, `.review-stars`, `.review-category`
- All new content blocks need `.reveal` class for IntersectionObserver animations

## AI PROMPT Doc

File ID: `1G7nAo3dQn6y5FIupTQWcXNOZxB0tFDmJqkCcbq4skw8` — Check this on every sync for pending instructions from the DM.
