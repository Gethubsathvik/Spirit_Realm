# =============================================
#   Upload Spirit Realm to GitHub
# =============================================

# Create .gitignore
@"
__pycache__/
*.pyc
*.db
*.log
"@ | Out-File -FilePath .gitignore -Encoding utf8

# Git setup
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/Gethubsathvik/Spirit_Realm.git
git push -u origin main
