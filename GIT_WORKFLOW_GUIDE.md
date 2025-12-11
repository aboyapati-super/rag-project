# Production Grade Git Workflow Guide

In professional software engineering, "pushing code" isn't just about saving your files to the cloud. It's about **History**, **Collaboration**, and **CI/CD** (Continuous Integration/Deployment).

Here is the step-by-step workflow for pushing code, with explanations of why each command matters in a production environment.

## 1. Check Your State
### Command
```bash
git status
```
### What it does
Lists which files have changed, which are new (untracked), and which are already staged for commit.

### Production Context
**"Look before you leap."**
In production, you accidentally committing a `.env` file with API keys, or a massive 1GB log file, can be a security disaster or break the build. Always run `git status` to ensure you are only committing what you intend to.

---

## 2. Review Your Changes
### Command
```bash
git diff
```
### What it does
Shows the exact lines of code changed (the "diffs") between your working directory and the last commit.

### Production Context
**"Self-Correction."**
Before you ask a peer to review your code, review it yourself. `git diff` lets you catch debug prints (`print("here")`), commented-out code, or temporary hacks you forgot to remove.
*Pro Tip*: Use `git diff --cached` to see changes you have already added to the staging area.

---

## 3. Stage Your Changes
### Command
```bash
git add <filename>
# OR all files (use with caution)
git add .
```
### What it does
Moves changes from your "Working Directory" to the "Staging Area". Only staged files will be included in the next commit.

### Production Context
**"Atomic Commits."**
In production, you should try to make "atomic" commits—commits that do one thing and one thing only (e.g., "Fix login bug" and "Update documentation" should be separate).
Using `git add <filename>` allows you to cherry-pick specific files for a commit while leaving others for later, keeping your project history clean and revertible.

---

## 4. Commit Your Work
### Command
```bash
git commit -m "feat: add user authentication middleware"
```
### What it does
Takes a snapshot of the staged files and saves it to your local git history with a descriptive message.

### Production Context
**"The History Log."**
A commit message is a communication tool. In production, we often follow **Conventional Commits** formats (e.g., `feat:`, `fix:`, `chore:`, `refactor:`) so that automated tools can generate changelogs or semantic version bumps.
*   **Bad**: `git commit -m "fix"`
*   **Good**: `git commit -m "fix: resolve null pointer exception in user service"`

---

## 5. Sync with Remote (Pull)
### Command
```bash
git pull origin <branch_name>
# Common production variation
git pull --rebase origin <branch_name>
```
### What it does
Fetches changes from the remote server (GitHub/GitLab) and merges them into your local code.

### Production Context
**"Conflict Resolution."**
Your teammates might have pushed code while you were working. You must pull their changes to ensure your code works with theirs *before* you push.
Using `--rebase` is preferred in many high-performance teams because it keeps the history linear (a straight line) rather than creating messy "Merge commit" loops.

---

## 6. Push to Remote
### Command
```bash
git push origin <branch_name>
```
### What it does
Uploads your local commits to the remote repository.

### Production Context
**"Triggering the Pipeline."**
In a production environment, pushing code is often the "Trigger".
1.  **CI (Continuous Integration)**: When you push, a server (like GitHub Actions) wakes up and runs your tests (`src/test.py`). If they fail, your code is rejected.
2.  **CD (Continuous Deployment)**: If you push to `main`, it might automatically deploy the app to production servers.
This is why `test.py` and `requirements.txt` are so critical—if they are wrong, the push fails the pipeline.

## Summary Checklist

1.  `git status` (Check what's happening)
2.  `git diff` (Self-review code)
3.  `git add .` (Stage files)
4.  `git commit -m "..."` (Save snapshot with meaning)
5.  `git pull --rebase` (Sync with team)
6.  `git push` (Upload and Deploy)

## 7. Branching Strategy (Production Best Practice)

You mentioned: *"one branch for dev and one for prod"*. This is perfectly correct and is very close to the standard **Git Flow** or **GitHub Flow**.

### The Standard "Dev -> Prod" Lifecycle

1.  **Main Branch (`main` / `master` / `prod`)**
    -   This is the "Source of Truth".
    -   The code here **MUST** be stable.
    -   It usually deploys automatically to Production.
    -   **Rule**: NEVER push directly to `main`. Always merge into it.

2.  **Develop Branch (`develop` / `dev`)**
    -   This is where integration happens.
    -   Developers push features here to test them together.
    -   It usually deploys to a "Staging" or "Dev" environment.

3.  **Feature Branches (`feat/new-login`)**
    -   Created by *you* for a specific task.
    -   Branched *off* `develop`.
    -   Merged *back into* `develop`.

### The Workflow Visualization

```
[Feature Branch]  -->  (Pull Request) -->  [Develop Branch]  -->  (Release/PR) -->  [Main Branch]
(Write Code)           (Review & Test)     (Integration Test)     (Deploy to Prod)   (Stable Live App)
```

### How to do this right now

1.  **Create Dev Branch**:
    ```bash
    git checkout -b develop
    ```
    *Now you are on `develop` branch. All new changes go here.*

2.  **Make Changes & Commit**:
    ```bash
    git add .
    git commit -m "feat: added new logging"
    ```

3.  **Push to Dev**:
    ```bash
    git push origin develop
    ```
    *Your code is now on the `develop` branch on GitHub.*

4.  **Merge to Prod (Main)**:
    *In production, we don't usually merge locally. We go to GitHub.com and open a **Pull Request (PR)** from `develop` to `main`.*
    
    If you want to do it via CLI (for solo projects):
    ```bash
    git checkout main      # Go to prod
    git merge develop      # Bring dev changes into prod
    git push origin main   # Update cloud prod
    ```
