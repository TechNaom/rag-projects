#!/usr/bin/env bash
set -euo pipefail

# ============================================================
# Internal Policy RAG POC — GitHub setup & push script
# ============================================================
# Run this FROM INSIDE the boa-rag-poc/ folder (after unzipping
# boa-rag-poc.zip). It will:
#   1. Check prerequisites (git, optionally GitHub CLI)
#   2. Initialize a git repo (skips if one already exists)
#   3. Write a .gitignore (Python cache files, .env secrets)
#   4. Stage and commit every file
#   5. Create the GitHub repo and push
#      - automatically, if you have GitHub CLI (`gh`) installed+authed
#      - otherwise, prints exact manual commands to run
#
# Usage:
#   chmod +x setup_and_push_to_github.sh
#   ./setup_and_push_to_github.sh [repo-name] [public|private]
#
# Example:
#   ./setup_and_push_to_github.sh policy-rag-poc private
#
# Prereqs:
#   - git installed (you have this already)
#   - Optional: GitHub CLI -> https://cli.github.com
#     If installed, run `gh auth login` ONE TIME before using this script.
#     Without gh, the script still does everything except the actual
#     repo-creation-and-push, which it'll print clear instructions for.
# ============================================================

REPO_NAME="${1:-policy-rag-poc}"
VISIBILITY="${2:-private}"

echo "=================================================="
echo " Step 1/5: Checking prerequisites"
echo "=================================================="
if ! command -v git >/dev/null 2>&1; then
  echo "ERROR: git is not installed. Install it first (e.g. https://git-scm.com/downloads) and re-run."
  exit 1
fi
echo "  git found: $(git --version)"

HAS_GH=false
if command -v gh >/dev/null 2>&1; then
  HAS_GH=true
  echo "  gh CLI found: $(gh --version | head -1)"
else
  echo "  gh CLI not found. The script will still set up git locally,"
  echo "  but you'll need to create the GitHub repo manually (instructions printed at the end)."
fi

echo ""
echo "=================================================="
echo " Step 2/5: Initializing git repository"
echo "=================================================="
if [ -d .git ]; then
  echo "  Already a git repo here - skipping 'git init'."
else
  git init
  echo "  Initialized empty git repo."
fi

echo ""
echo "=================================================="
echo " Step 3/5: Writing .gitignore"
echo "=================================================="
cat > .gitignore << 'EOF'
__pycache__/
*.pyc
.env
*.egg-info/
.DS_Store
EOF
echo "  .gitignore written (excludes Python cache files and .env secrets)."

echo ""
echo "=================================================="
echo " Step 4/5: Staging and committing files"
echo "=================================================="
git add -A
if git diff --cached --quiet 2>/dev/null; then
  echo "  Nothing new to commit (already committed)."
else
  git commit -m "Internal Policy RAG POC (fictional bank corpus)

- 12 synthetic banking HR/compliance policy documents
- Markdown-header-aware chunking pipeline
- Local TF-IDF+SVD embeddings (network-sandbox-safe, swappable for neural embeddings)
- ChromaDB vector store (persisted)
- Retrieval + Claude generation chain
- Golden-set retrieval evaluation (Recall@3 86.7%, MRR 0.789)"
  echo "  Committed."
fi

echo ""
echo "=================================================="
echo " Step 5/5: Creating GitHub repo and pushing"
echo "=================================================="
if [ "$HAS_GH" = true ]; then
  if git remote get-url origin >/dev/null 2>&1; then
    echo "  Remote 'origin' already set - pushing to it directly."
    git branch -M main
    git push -u origin main
  else
    gh repo create "$REPO_NAME" --"$VISIBILITY" --source=. --remote=origin --push
  fi
  echo ""
  echo "  Done! Your repo:"
  gh repo view --json url -q .url 2>/dev/null || true
else
  echo "  gh CLI not available - do this manually:"
  echo ""
  echo "  1. Go to https://github.com/new and create a repo named '$REPO_NAME'"
  echo "     IMPORTANT: do NOT initialize it with a README, license, or .gitignore"
  echo "     (this script already created a .gitignore and you'll get conflicts otherwise)"
  echo ""
  echo "  2. Then run these three commands:"
  echo "     git remote add origin https://github.com/<your-username>/$REPO_NAME.git"
  echo "     git branch -M main"
  echo "     git push -u origin main"
  echo ""
  echo "  (First push will prompt for GitHub login - use a Personal Access Token"
  echo "   as the password if prompted; GitHub stopped accepting account passwords"
  echo "   for git operations. Create one at https://github.com/settings/tokens )"
fi
