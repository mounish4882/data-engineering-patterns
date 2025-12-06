# 🚀 New Repository Setup Guide

This guide will help you set up your new `data-engineering-patterns` repository from scratch with proper branch protection and professional structure.

---

## 📋 Step 1: Create Repository on GitHub

1. **Go to**: https://github.com/new

2. **Configure:**
   ```
   Repository name: data-engineering-patterns
   Description: Production-grade data engineering patterns for industrial IoT and manufacturing at scale
   Visibility: ✅ Public (for portfolio visibility)

   Initialize:
   ✅ Add a README file: NO (we have our own)
   ✅ Add .gitignore: NO (we have our own)
   ✅ Choose a license: MIT License
   ```

3. **Click**: "Create repository"

---

## 📋 Step 2: Clone and Setup Locally

```bash
# Clone your new empty repository
git clone https://github.com/YOUR_USERNAME/data-engineering-patterns.git
cd data-engineering-patterns

# Verify you're in the right place
pwd  # Should show: /path/to/data-engineering-patterns
```

---

## 📋 Step 3: Copy All Files from This Repo

### Option A: Manual Copy

```bash
# From your OLD repo directory (where you are now)
# Copy all files to your NEW repo

# Navigate to where you want the files
cd /path/to/NEW/data-engineering-patterns

# Copy everything from old repo (adjust path)
cp -r /home/user/data-engineering-patterns/* .
cp -r /home/user/data-engineering-patterns/.github .
cp -r /home/user/data-engineering-patterns/.gitignore .

# Remove files you don't need
rm NEW_REPO_SETUP.md  # This guide
rm OPTION_B_PROMPT.md # Optional: keep or remove
```

### Option B: Use This Script

```bash
#!/bin/bash
# save as: copy-to-new-repo.sh

SOURCE_DIR="/home/user/data-engineering-patterns"
TARGET_DIR="$HOME/projects/data-engineering-patterns"  # Adjust this!

# Copy all necessary files
cp -r $SOURCE_DIR/README.md $TARGET_DIR/
cp -r $SOURCE_DIR/CONTRIBUTING.md $TARGET_DIR/
cp -r $SOURCE_DIR/LICENSE $TARGET_DIR/
cp -r $SOURCE_DIR/.gitignore $TARGET_DIR/
cp -r $SOURCE_DIR/.github $TARGET_DIR/

# Copy initial patterns (when created)
# cp -r $SOURCE_DIR/01-authentication-security $TARGET_DIR/
# cp -r $SOURCE_DIR/02-schema-evolution $TARGET_DIR/

echo "✅ Files copied successfully!"
```

---

## 📋 Step 4: Make Your First Commit

```bash
# In your NEW repository directory
cd /path/to/data-engineering-patterns

# Check what you have
git status

# Add all files
git add .

# Create your first commit
git commit -m "feat: initial repository setup

- Add comprehensive README with pattern catalog
- Add contribution guidelines
- Add GitHub Actions CI/CD workflows
- Add PR and issue templates
- Configure .gitignore for data engineering projects

This establishes the foundation for a production-grade
data engineering patterns repository focused on
manufacturing and industrial IoT at scale."

# Push to main (first commit goes directly to main)
git push origin main
```

---

## 📋 Step 5: Set Up Branch Protection

### On GitHub:

1. **Go to**: Your repository → Settings → Branches

2. **Click**: "Add branch protection rule"

3. **Configure Branch Protection for `main`:**

   ```
   Branch name pattern: main

   ✅ Require a pull request before merging
      ✅ Require approvals: 1
      ✅ Dismiss stale pull request approvals when new commits are pushed
      ✅ Require review from Code Owners (optional - for later)

   ✅ Require status checks to pass before merging
      ✅ Require branches to be up to date before merging
      Status checks that are required:
         - lint (once CI runs for first time)
         - markdown-lint
         - validate-structure

   ✅ Require conversation resolution before merging

   ✅ Require linear history (keeps history clean)

   ✅ Do not allow bypassing the above settings
      (Applies even to admins - keeps you disciplined!)

   ✅ Restrict who can push to matching branches
      Add: YOUR_USERNAME (only you can merge)
   ```

4. **Click**: "Create" or "Save changes"

---

## 📋 Step 6: Verify Setup

### Test Branch Protection

```bash
# Try to push directly to main (should fail after protection is set)
echo "test" >> README.md
git add README.md
git commit -m "test: verify branch protection"
git push origin main
# ❌ Should get: "required status checks" or "pull request required"

# Clean up test
git reset --hard HEAD~1
```

### Verify CI/CD

1. Go to: Actions tab on GitHub
2. You should see workflows ready to run
3. Make a test PR to trigger them

---

## 📋 Step 7: Create Your First PR (Practice)

```bash
# Create a feature branch
git checkout -b feature/update-readme

# Make a small change
echo -e "\n---\n\n*Repository initialized: $(date)*" >> README.md

# Commit
git add README.md
git commit -m "docs: add repository initialization timestamp"

# Push
git push origin feature/update-readme

# Go to GitHub and create PR
# You'll see:
# - CI/CD checks running
# - PR template auto-populated
# - Branch protection requiring approval
```

**On GitHub:**
1. Go to Pull Requests → New Pull Request
2. Base: `main` ← Compare: `feature/update-readme`
3. Fill in the PR template
4. Create Pull Request
5. Wait for CI checks to pass
6. Approve and Merge (you can approve your own for now)
7. Delete the feature branch after merge

---

## 📋 Step 8: Development Workflow (Going Forward)

### Every Feature Follows This Process:

```bash
# 1. Start from latest main
git checkout main
git pull origin main

# 2. Create feature branch
git checkout -b feature/add-kafka-pattern

# 3. Make changes
# ... create files, write code ...

# 4. Commit with good messages
git add .
git commit -m "feat: add Kafka SASL/SSL authentication pattern

- Add comprehensive authentication guide
- Include troubleshooting playbook
- Add code examples with SASL mechanisms
- Add Databricks secrets integration example"

# 5. Push to remote
git push origin feature/add-kafka-pattern

# 6. Create Pull Request on GitHub
#    - Fill in PR template
#    - Wait for CI checks
#    - Review your own changes
#    - Merge when ready

# 7. Clean up
git checkout main
git pull origin main
git branch -d feature/add-kafka-pattern
```

---

## 📋 Step 9: Recommended GitHub Settings

### General Settings

**Go to**: Settings → General

```
✅ Features:
   ✅ Wikis (for extended documentation)
   ✅ Issues (for tracking work)
   ✅ Discussions (for Q&A)

✅ Pull Requests:
   ✅ Allow squash merging (keep history clean)
   ✅ Allow auto-merge
   ✅ Automatically delete head branches

✅ Archives:
   ❌ Include Git LFS objects (not needed)
```

### About Section

**Go to**: Main repository page → About (gear icon)

```
Description: Production-grade data engineering patterns for industrial IoT and manufacturing at scale

Website: (your portfolio site or LinkedIn)

Topics (tags):
   - data-engineering
   - apache-spark
   - apache-kafka
   - delta-lake
   - databricks
   - manufacturing
   - iot
   - streaming
   - python
   - pyspark
```

### Social Preview

**Go to**: Settings → General → Social Preview

- Upload a custom image (1280x640px)
- Or let GitHub auto-generate from README

---

## 📋 Step 10: Add Project Management (Optional)

### Create GitHub Project

1. **Go to**: Projects → New Project
2. **Template**: "Team backlog"
3. **Name**: "Data Engineering Patterns Roadmap"

**Add Issues for Patterns:**
```markdown
- [ ] #1 Kafka SASL/SSL Authentication
- [ ] #2 Delta Lake Schema Evolution
- [ ] #3 MAP Type Flattening
- [ ] #4 Dimensional Modeling
- [ ] #5 Spark Performance Optimization
- [ ] #6 Databricks Deployment
```

---

## ✅ Verification Checklist

After setup, verify:

- [ ] Repository is public and visible
- [ ] README displays correctly on GitHub
- [ ] CI/CD workflows are present in Actions tab
- [ ] Branch protection is active on `main`
- [ ] PR template auto-populates on new PRs
- [ ] Issues can be created with templates
- [ ] License file is present
- [ ] Topics/tags are added
- [ ] About section is filled out

---

## 🎯 What's Next?

### Immediate Next Steps:

1. **Share your repository**
   - Add link to LinkedIn profile
   - Tweet about it
   - Share in data engineering communities

2. **Start building patterns**
   - Pick a pattern from OPTION_B_PROMPT.md
   - Create a feature branch
   - Build it out
   - Submit PR
   - Merge!

3. **Iterate**
   - Add patterns weekly
   - Improve documentation
   - Engage with contributors

### First Patterns to Build:

**Week 1:**
- Kafka SASL/SSL Authentication (high impact)

**Week 2:**
- Delta Lake Schema Evolution

**Week 3:**
- Dimensional Modeling Basics

---

## 🆘 Troubleshooting

### "Can't push to main"
✅ **This is correct!** Branch protection is working.
   Solution: Create a PR instead.

### "CI checks failing"
1. Check the Actions tab for details
2. Fix the issues locally
3. Push again - checks will re-run

### "PR can't be merged"
- Ensure all CI checks pass
- Resolve any merge conflicts
- Get required approvals

---

## 📚 Resources

**Git Best Practices:**
- [Conventional Commits](https://www.conventionalcommits.org/)
- [GitHub Flow](https://guides.github.com/introduction/flow/)

**GitHub Features:**
- [Branch Protection](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches)
- [GitHub Actions](https://docs.github.com/en/actions)

---

## 🎉 You're All Set!

Your repository is now:
- ✅ Professionally structured
- ✅ Branch-protected
- ✅ CI/CD enabled
- ✅ Ready for contributions
- ✅ Portfolio-ready

**Start building amazing patterns!** 🚀

---

**Questions?** Open an issue in the repository or reach out!

*This setup creates a foundation for a world-class data engineering patterns repository.*
