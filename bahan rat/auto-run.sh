#!/bin/bash
# ═══════════════════════════════════════════════════════════════
#   AUTO PUSH TO GITHUB + BUILD APK
#   Credit : XaztanDEV
# ═══════════════════════════════════════════════════════════════

echo "🚀 Ghost RAT Auto Push"
echo "Credit : XaztanDEV"

# Init git
git init
git add .
git commit -m "Ghost RAT update - $(date)"
git branch -M main

# Push
read -p "GitHub username: " USER
read -p "Repo name: " REPO
git remote add origin https://github.com/$USER/$REPO.git
git push -u origin main

echo "✅ Selesai! Cek build di:"
echo "   https://github.com/$USER/$REPO/actions"