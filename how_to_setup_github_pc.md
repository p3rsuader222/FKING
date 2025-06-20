Since you want a **short, step-by-step guide** to connect a new project on your PC to a new GitHub repository using **VS Code**, I’ll provide a concise, beginner-friendly process to set up a project from scratch and enable easy syncing. This assumes you’re starting a new project (e.g., named `NEWPROJECT`) under your GitHub user `p3rsuader222`, with files in a local folder (e.g., `D:\relocationasonedrive\LEARNCODE\NEWPROJECT`). I’ll include Git LFS for large files (e.g., CSVs), handle line-ending issues, and provide a batch file and VS Code steps for syncing, considering your prior setup with `FKING` and potential OneDrive issues.

### Assumptions
- **GitHub Account**: You’re logged in as `p3rsuader222`.
- **Git Installed**: Run `git --version` in PowerShell to confirm. If not, download from [git-scm.com](https://git-scm.com/).
- **Git LFS Installed**: Run `git lfs version`. If not, download from [git-lfs.github.com](https://git-lfs.github.com/).
- **VS Code Installed**: Available for editing and syncing.
- **Project Folder**: Files in `D:\relocationasonedrive\LEARNCODE\NEWPROJECT` (adjust if different).
- **PowerShell**: You’re using PowerShell (as seen previously).

### Short Step-by-Step Guide

#### Step 1: Create Local Project Folder
1. **Create Folder**:
   - Open File Explorer, navigate to `D:\relocationasonedrive\LEARNCODE`.
   - Create a folder named `NEWPROJECT`.
   - Copy your project files (e.g., `data/raw/m5/1_calendar.csv`, `.md` files) into `D:\relocationasonedrive\LEARNCODE\NEWPROJECT`.
2. **Verify Files**:
   ```powershell
   dir D:\relocationasonedrive\LEARNCODE\NEWPROJECT -Recurse
   ```
   - Ensure files like CSVs are present.
3. **Check File Sizes** (for Git LFS):
   ```powershell
   dir D:\relocationasonedrive\LEARNCODE\NEWPROJECT\data\*.csv | Select-Object Name, Length
   ```
   - Note files >104,857,600 bytes (100 MB).

#### Step 2: Create GitHub Repository
1. **Open Browser**:
   - Go to [github.com](https://github.com/), log in as `p3rsuader222`.
2. **Create Repository**:
   - Click `+` > `New repository`.
   - **Name**: `NEWPROJECT`.
   - **Public/Private**: Choose `Public` (or `Private`).
   - **Initialize**: **Uncheck** `README`, `.gitignore`, license.
   - Click `Create repository`.
3. **Copy URL**:
   - On `https://github.com/p3rsuader222/NEWPROJECT`, click `Code`, copy: `https://github.com/p3rsuader222/NEWPROJECT.git`.

#### Step 3: Initialize Git Repository
1. **Open PowerShell**:
   - Press `Win + R`, type `powershell`, press `Enter`.
2. **Navigate to Folder**:
   ```powershell
   cd D:\relocationasonedrive\LEARNCODE\NEWPROJECT
   ```
3. **Initialize Git**:
   ```powershell
   git init
   ```
4. **Set Git Config**:
   ```powershell
   git config --global user.name "p3rsuader222"
   git config --global user.email "dovydas.dervinis@gmail.com"
   git config --global core.autocrlf false
   git config --global credential.helper wincred
   ```

#### Step 4: Set Up Git LFS and `.gitattributes`
1. **Install Git LFS**:
   ```powershell
   git lfs install
   ```
2. **Create `.gitattributes`**:
   - Open VS Code: `File > Open Folder > D:\relocationasonedrive\LEARNCODE\NEWPROJECT`.
   - Right-click in Explorer > `New File` > `.gitattributes`.
   - Paste:
     ```
     *.csv -text
     *.md text eol=lf
     *.txt text eol=lf
     data/*.csv filter=lfs diff=lfs merge=lfs -text
     ```
   - Save (`Ctrl+S`).
3. **Track Large CSVs**:
   ```powershell
   git lfs track "data/*.csv"
   ```

#### Step 5: Create `.gitignore`
1. **Create File**:
   - In VS Code, right-click > `New File` > `.gitignore`.
   - Paste:
     ```
     *.tmp
     *.bak
     sync_repo.bat
     sync_log.txt
     ```
   - Save.

#### Step 6: Stage and Commit Files
1. **Stage Files**:
   - In VS Code, go to Source Control (`Ctrl+Shift+G`).
   - Click `+` to stage all files or `Stage All Changes` in `...` menu.
   - Or in PowerShell:
     ```powershell
     git add .
     ```
2. **Verify**:
   ```powershell
   git status
   ```
   - Ensure CSVs, `.gitattributes`, `.gitignore` are listed.
3. **Commit**:
   - In VS Code, enter “Initial commit with all project files” in the message box, click checkmark (`Commit`).
   - Or:
     ```powershell
     git commit -m "Initial commit with all project files"
     ```

#### Step 7: Connect to GitHub and Push
1. **Add Remote**:
   ```powershell
   git remote add origin https://github.com/p3rsuader222/NEWPROJECT.git
   ```
2. **Set Main Branch**:
   ```powershell
   git branch -m main
   ```
3. **Push**:
   - In VS Code: Source Control > `...` > `Push`.
   - Or:
     ```powershell
     git push -u origin main
     ```
   - Enter GitHub username (`p3rsuader222`) and password/PAT if prompted.
   - Create PAT if needed: GitHub > Profile > `Settings` > `Developer settings` > `Personal access tokens` > `Generate new token` > select `repo` scope > copy token.

#### Step 8: Create Batch File for Syncing
1. **Create `sync_repo.bat`**:
   - In VS Code, right-click > `New File` > `sync_repo.bat`.
   - Paste:
     
     @echo off
     setlocal EnableDelayedExpansion
     set REPO_PATH=D:\relocationasonedrive\LEARNCODE\NEWPROJECT
     set LOG_FILE=%REPO_PATH%\sync_log.txt
     echo Sync started at %DATE% %TIME% > "%LOG_FILE%"
     cd /d "%REPO_PATH%" || (
         echo ERROR: Failed to navigate to %REPO_PATH% >> "%LOG_FILE%"
         echo ERROR: Failed to navigate to %REPO_PATH%
         pause
         exit /b 1
     )
     git lfs install >> "%LOG_FILE%" 2>&1
     git pull origin main >> "%LOG_FILE%" 2>&1 || (
         echo ERROR: Failed to pull changes >> "%LOG_FILE%"
         echo ERROR: Failed to pull changes
         pause
         exit /b 1
     )
     git status >> "%LOG_FILE%" 2>&1
     git add . >> "%LOG_FILE%" 2>&1
     git commit -m "Auto-sync changes" >> "%LOG_FILE%" 2>&1 || (
         echo No changes to commit >> "%LOG_FILE%"
         echo No changes to commit
     )
     git push origin main >> "%LOG_FILE%" 2>&1 || (
         echo ERROR: Failed to push to GitHub >> "%LOG_FILE%"
         echo ERROR: Failed to push to GitHub
         pause
         exit /b 1
     )
     git status >> "%LOG_FILE%" 2>&1
     echo Sync completed successfully at %DATE% %TIME% >> "%LOG_FILE%"
     echo Sync completed successfully! Check %LOG_FILE% for details.
     echo Files updated at https://github.com/p3rsuader222/NEWPROJECT
     pause
     
   - Save.
2. **Test**:
   ```powershell
   cd D:\relocationasonedrive\LEARNCODE\NEWPROJECT
   .\sync_repo.bat
   ```

#### Step 9: Sync Changes
1. **PC to GitHub**:
   - Edit a file in VS Code, save.
   - Source Control: Stage (`+`) > Commit (message: “Updated files”) > Push (`... > Push`).
   - Or run `sync_repo.bat`.
2. **GitHub to PC**:
   - Edit a file on `https://github.com/p3rsuader222/NEWPROJECT` (web interface).
   - Run:
     ```powershell
     git pull origin main
     ```
   - Or run `sync_repo.bat`.

#### Step 10: Verify
- Check `https://github.com/p3rsuader222/NEWPROJECT` for files and commits.
- Confirm `sync_log.txt` shows successful syncs:
  ```powershell
  Get-Content D:\relocationasonedrive\LEARNCODE\NEWPROJECT\sync_log.txt
  ```

#### Troubleshoot
1. **Files Missing**:
   ```powershell
   git status
   dir D:\relocationasonedrive\LEARNCODE\NEWPROJECT\data
   ```
   - Check `.gitignore`.
2. **Large Files**:
   - If `git push` fails with `file exceeds 100 MB`, ensure Git LFS and `.gitattributes`.
3. **OneDrive**:
   - If `D:\relocationasonedrive` is in OneDrive:
     ```powershell
     dir C:\Users\dovyd\OneDrive\relocationasonedrive
     ```
     - Update `sync_repo.bat`:
       ```batch
       set REPO_PATH=C:\Users\dovyd\OneDrive\relocationasonedrive\LEARNCODE\NEWPROJECT
       ```
   - Or move:
     ```powershell
     Move-Item -Path D:\relocationasonedrive\LEARNCODE\NEWPROJECT -Destination D:\LEARNCODE
     ```

This covers setting up a new project with VS Code and GitHub. Let me know if you need clarification or hit any issues!
