---
name: skill-git-publish
description: "Turn a WorkBuddy skills folder into a Git repo and publish it to GitHub via GitHub Desktop. Use when the user wants to version-control, back up, share, or open-source their skills. Covers local git init + first commit (via the agent) and remote publishing + daily sync (via GitHub Desktop). Triggers: 把 skills 上传 GitHub, 用 GitHub Desktop 管理 skill, 初始化技能仓库, publish skills to github, git init skills."
agent_created: true
---

# Skill: Publish Skills to GitHub

Turn a WorkBuddy `skills` folder into a Git repository, then manage it through GitHub Desktop. The agent handles **local repo creation**; the user completes **remote publishing** in GitHub Desktop (account authorization cannot be done by the agent).

---

## When to use
- "把我的 skills 文件夹上传到 GitHub"
- "用 GitHub Desktop 管理这个 Skill / 文件夹"
- "初始化 skills 仓库并开源/备份"

## Scope decision (ask before acting)
This skill works on **any folder**, but the typical target is the WorkBuddy skills dir:
- **User-level**: `~/.workbuddy/skills` (all projects, recommended for personal backups)
- **Single skill**: `~/.workbuddy/skills/<skill-name>` (one skill per repo)

Also confirm **private vs public** — default recommendation is **private** (skills may contain personal workflows or API keys).

---

## Step 1 — Pre-checks (agent, read-only)

Run before initializing. Do NOT create the repo if these reveal problems.

1. **Git available?**
   ```bash
   git --version
   ```
2. **GitHub Desktop installed?**
   ```bash
   ls -d "/Applications/GitHub Desktop.app"
   ```
   (macOS path; adjust for other OS)
3. **Already a repo?**
   ```bash
   cd <TARGET_DIR> && git rev-parse --is-inside-work-tree 2>&1 | head -1
   ```
   If "true", skip `git init` and go straight to commit (or tell the user it's already a repo).
4. **Secret scan** (critical before publishing personal skills):
   ```bash
   cd <TARGET_DIR> && grep -rniE "api[_-]?key|secret|token|password|passwd|bearer|sk-[a-z0-9]|ghp_|private[_-]?key" . 2>/dev/null | grep -viE "your[_ -]?api|<|placeholder|example|xxxx|如.*密钥|填入|替换|opaque token|tokenization|context window|token limit"
   ```
   If real credentials appear, STOP and tell the user to remove them (or add to `.gitignore`) before proceeding.

---

## Step 2 — Local repo (agent executes)

```bash
# 1. .gitignore (exclude junk; commit .DS_Store junk not needed)
cd <TARGET_DIR>
cat > .gitignore <<'EOF'
# macOS
.DS_Store

# Python
*.pyc
__pycache__/
EOF

# 2. init + commit
git init -b main
git add .
git -c user.name="<USER>" -c user.email="<USER>@example.com" commit -m "Initial commit: <repo name>"
```

> **Placeholder author note**: The first commit uses a placeholder email. It's harmless — GitHub Desktop later commits with the signed-in account. To fix retroactively before publishing, the user (or agent) can run:
> ```bash
> git commit --amend --reset-author   # after `git config user.name/user.email`
> ```
> Or just leave it; subsequent GitHub Desktop commits carry the correct identity.

> **`.git` is safe**: A `.git` directory does NOT affect WorkBuddy reading/running the skills. Leave it in place.

---

## Step 3 — Publish via GitHub Desktop (USER does this)

GitHub Desktop cannot be driven by the agent (needs account login). Hand these exact steps to the user:

**A. Add the local repo**
1. Open GitHub Desktop
2. `File` → `Add Local Repository...` (or `Cmd+O`)
3. Select `<TARGET_DIR>`
   - Hidden dirs (e.g. `~/.workbuddy`): in the file picker press `Cmd+Shift+.` to reveal hidden folders
4. It detects the existing repo + first commit

**B. Sign in (if not already)**
- `GitHub Desktop` → `Settings` → `Accounts` → `Sign in` (browser authorizes your GitHub account)

**C. Publish**
1. Click **`Publish repository`**
2. Name it (e.g. `workbuddy-skills`)
3. **Check `Keep this code private`** (recommended default; change to public later on github.com if desired)
4. Click `Publish repository`

---

## Step 4 — Daily sync (USER, recurring)

After editing any skill file in the folder:
1. GitHub Desktop → `Changes` lists modifications
2. Fill **Summary** (bottom-left), click `Commit to main`
3. Click `Push origin` (top-right) to send to GitHub
4. If remote changed elsewhere: `Fetch origin` / `Pull origin` first

---

## Post-publish checklist
- [ ] Local repo created with first commit
- [ ] Secret scan passed (no real credentials committed)
- [ ] Repo added to GitHub Desktop
- [ ] Published as **private** (unless user chose public)
- [ ] User knows daily `Commit` → `Push origin` flow
- [ ] `.gitignore` excludes `.DS_Store` / `__pycache__`

---

## Common pitfalls
- **Hidden folder not visible in picker** → `Cmd+Shift+.` reveals it
- **Published public by accident** → change visibility at github.com/settings or repo Settings → Danger Zone
- **Accidentally committed a secret** → rotate the secret immediately, then `git filter-repo` / remove + force-push (or just delete the repo if not yet shared)
- **`.git` breaks WorkBuddy** → it does NOT; ignore this fear
- **Author shows "tom@example.com"** → harmless; fixed by GitHub Desktop commits automatically
