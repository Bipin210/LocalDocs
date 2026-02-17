# GitHub Push Checklist

## ✅ Files TO INCLUDE (Source Code):
- [x] app.py
- [x] requirements.txt
- [x] setup.sh
- [x] start.sh
- [x] README.md
- [x] QUICKSTART.md
- [x] LICENSE
- [x] .gitignore
- [x] utils/ (all .py files)
- [x] templates/ (all .html files)
- [x] static/ (css, js files)
- [x] uploads/.gitkeep (empty directory marker)
- [x] outputs/.gitkeep (empty directory marker)

## ❌ Files TO EXCLUDE (Already in .gitignore):
- [x] venv/ (virtual environment)
- [x] __pycache__/ (Python cache)
- [x] uploads/* (user uploaded files)
- [x] outputs/* (generated files)
- [x] *.pyc, *.pyo (compiled Python)
- [x] .DS_Store, Thumbs.db (OS files)
- [x] .vscode/, .idea/ (IDE settings)
- [x] *.log (log files)

## 📋 Pre-Push Commands:

```bash
cd /home/leapfrog/poc/converter

# Initialize git (if not already done)
git init

# Add all files (respects .gitignore)
git add .

# Check what will be committed
git status

# Verify no sensitive files are staged
git diff --cached --name-only

# Commit
git commit -m "Initial commit: PDF Tools - Privacy-first document processor"

# Add remote (replace with your GitHub repo URL)
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git

# Push to GitHub
git push -u origin main
```

## 🔍 Final Verification:

Run these commands to verify nothing sensitive is included:

```bash
# Check for any uploaded files
git ls-files | grep uploads/

# Check for any output files  
git ls-files | grep outputs/

# Should only show .gitkeep files
```

## 📝 Recommended GitHub Repository Settings:

**Repository Name Ideas:**
- pdf-tools-local
- localdocs
- privacy-pdf-tools
- offline-pdf-converter

**Description:**
"Privacy-first PDF and image processing toolkit that runs entirely on your local machine. No cloud, no tracking, no limits."

**Topics/Tags:**
- pdf
- converter
- privacy
- offline
- python
- flask
- local-first
- document-processing
- image-compression

**README Badges to Add (optional):**
- Python version
- License
- Contributions welcome
