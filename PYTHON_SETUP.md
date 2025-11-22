# Python Setup and Troubleshooting Guide for Windows

This guide provides detailed solutions for the common Windows Python path issue and comprehensive setup instructions for the Fabazzz application.

## Table of Contents

- [Understanding the Problem](#understanding-the-problem)
- [Quick Fix](#quick-fix)
- [Detailed Solutions](#detailed-solutions)
- [Verification Steps](#verification-steps)
- [Common Issues](#common-issues)
- [Best Practices](#best-practices)

## Understanding the Problem

### The Error Message

```
Python was not found; run without arguments to install from the Microsoft Store,
or disable this shortcut from Settings > Apps > Advanced app settings > App execution aliases.
```

### Why This Happens

Windows 10 and 11 include "App Execution Aliases" that redirect `python` and `python3` commands to the Microsoft Store. These aliases take precedence over actual Python installations, causing this error even when Python is properly installed.

## Quick Fix

**The fastest solution is to disable the Microsoft Store aliases:**

1. Press `Win + I` to open Settings
2. Navigate to: **Apps** → **Apps & features** → **App execution aliases**
3. Scroll down to find:
   - **App Installer (python.exe)**
   - **App Installer (python3.exe)**
4. Toggle **both** to **OFF**
5. Open a new terminal and test: `python --version`

## Detailed Solutions

### Solution 1: Disable App Execution Aliases

**When to use:** You already have Python installed but Windows is not finding it.

**Steps:**

1. **Open Windows Settings:**
   - Press `Win + I`
   - Or search for "Settings" in the Start menu

2. **Navigate to App Execution Aliases:**
   - Click **Apps**
   - Click **Apps & features** (left sidebar)
   - Scroll down and click **App execution aliases**
   - Alternatively: Click **Advanced app settings** → **App execution aliases**

3. **Disable Python Aliases:**
   - Find entries labeled "App Installer python.exe"
   - Find entries labeled "App Installer python3.exe"
   - Toggle switches to **OFF** for both

4. **Restart Terminal:**
   - Close all PowerShell/Command Prompt windows
   - Open a new terminal
   - Test: `python --version`

### Solution 2: Install Python Properly

**When to use:** Python is not installed, or you need a fresh installation.

**Steps:**

1. **Download Python:**
   ```
   Visit: https://www.python.org/downloads/
   Download: Python 3.8 or higher (3.11+ recommended)
   ```

2. **Run the Installer:**
   - Double-click the downloaded `.exe` file
   - ✅ **CRITICAL:** Check **"Add Python to PATH"** at the bottom
   - Select **"Customize installation"** for more options, or
   - Select **"Install Now"** for default settings

3. **Customization Options (if chosen):**
   - ✅ pip
   - ✅ tcl/tk and IDLE
   - ✅ Python test suite (optional)
   - ✅ py launcher (recommended for multiple versions)

4. **Advanced Options:**
   - ✅ Install for all users (requires admin rights)
   - ✅ Add Python to environment variables
   - ✅ Precompile standard library
   - Choose installation directory (default is fine)

5. **Complete Installation:**
   - Click **Install**
   - Wait for completion
   - Click **Close**

6. **Verify:**
   ```powershell
   python --version
   pip --version
   ```

### Solution 3: Manual PATH Configuration

**When to use:** Python is installed but not in system PATH.

**Steps:**

1. **Locate Python Installation:**

   Common locations:
   ```
   C:\Users\<YourUsername>\AppData\Local\Programs\Python\Python3xx\
   C:\Python3xx\
   C:\Program Files\Python3xx\
   ```

   To find it:
   ```powershell
   # Search for python.exe
   where.exe python

   # Or use Python launcher
   py -c "import sys; print(sys.executable)"
   ```

2. **Open Environment Variables:**
   - Press `Win + R`
   - Type: `sysdm.cpl` and press Enter
   - Click **Advanced** tab
   - Click **Environment Variables** button

3. **Edit PATH Variable:**

   **Option A - User Variables (recommended):**
   - Under "User variables", find **Path**
   - Click **Edit**
   - Click **New**
   - Add: `C:\Users\<YourUsername>\AppData\Local\Programs\Python\Python3xx\`
   - Click **New** again
   - Add: `C:\Users\<YourUsername>\AppData\Local\Programs\Python\Python3xx\Scripts\`
   - Click **OK**

   **Option B - System Variables (requires admin):**
   - Under "System variables", find **Path**
   - Follow same steps as above

4. **Apply Changes:**
   - Click **OK** on all dialogs
   - **Important:** Restart all terminal windows
   - Or restart your computer for system-wide effect

5. **Verify:**
   ```powershell
   # Close all terminals first!
   # Open new PowerShell
   python --version
   ```

## Verification Steps

After applying any solution, verify Python is working correctly:

```powershell
# Step 1: Check Python version
python --version
# Expected output: Python 3.x.x

# Step 2: Check pip version
pip --version
# Expected output: pip 2x.x.x from C:\...\python3xx\lib\site-packages\pip (python 3.x)

# Step 3: Test Python interpreter
python -c "print('Python is working correctly!')"
# Expected output: Python is working correctly!

# Step 4: Check Python executable location
python -c "import sys; print(sys.executable)"
# Expected output: C:\...\Python\Python3xx\python.exe

# Step 5: Verify pip can install packages
pip install --upgrade pip
# Should complete without errors
```

## Common Issues

### Issue 1: "python is not recognized" even after adding to PATH

**Solutions:**
- Restart your terminal (required!)
- Restart your computer (for system PATH changes)
- Check PATH order (Python should come before Windows\System32)
- Ensure no typos in PATH entries
- Verify paths actually exist in File Explorer

### Issue 2: Multiple Python Versions Installed

**Use Windows Python Launcher:**

```powershell
# List all installed Python versions
py --list

# Run specific version
py -3.12 script.py  # Use Python 3.12
py -3.8 script.py   # Use Python 3.8

# Use latest Python 3
py -3 script.py

# Open specific Python interpreter
py -3.12
```

**Set default version:**
Create/edit `py.ini` in `C:\Windows\py.ini`:
```ini
[defaults]
python=3.12
```

### Issue 3: Permission Errors During Installation

**Solutions:**
- Run installer as Administrator
- Or install for current user only (uncheck "for all users")
- Disable antivirus temporarily during installation
- Check disk space (need ~100MB minimum)

### Issue 4: pip Not Working

**Solutions:**

```powershell
# Reinstall pip
python -m ensurepip --upgrade

# Or download get-pip.py
# Visit: https://bootstrap.pypa.io/get-pip.py
# Save file and run:
python get-pip.py

# Verify pip
python -m pip --version
```

### Issue 5: SSL Certificate Errors

**Solutions:**

```powershell
# Upgrade pip
python -m pip install --upgrade pip

# Install package with trusted host (temporary workaround)
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org package-name

# Update certificates
pip install --upgrade certifi
```

## Best Practices

### 1. Use Virtual Environments

**Why:** Isolates project dependencies, prevents conflicts.

```powershell
# Create virtual environment
python -m venv venv

# Activate (Windows PowerShell)
venv\Scripts\Activate.ps1

# Activate (Windows Command Prompt)
venv\Scripts\activate.bat

# Activate (Git Bash)
source venv/Scripts/activate

# Deactivate
deactivate

# Install dependencies in venv
pip install -r requirements.txt
```

**If PowerShell Execution Policy Blocks Activation:**

```powershell
# Check current policy
Get-ExecutionPolicy

# Allow for current user
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Or run with bypass
powershell -ExecutionPolicy Bypass -File venv\Scripts\Activate.ps1
```

### 2. Keep Python Updated

```powershell
# Check current version
python --version

# Update pip
python -m pip install --upgrade pip

# Update setuptools and wheel
pip install --upgrade setuptools wheel
```

### 3. Use Requirements Files

```powershell
# Create requirements file
pip freeze > requirements.txt

# Install from requirements
pip install -r requirements.txt

# Update all packages
pip list --outdated
pip install --upgrade package-name
```

### 4. Clean Installation (If All Else Fails)

1. **Uninstall Python:**
   - Settings → Apps → Find Python → Uninstall
   - Manually delete Python folders if they exist:
     - `C:\Users\<Username>\AppData\Local\Programs\Python\`
     - `C:\Python3xx\`

2. **Clean Registry (Advanced):**
   - Press `Win + R`, type `regedit`
   - Navigate to: `HKEY_CURRENT_USER\Software\Python`
   - Delete Python key (backup first!)
   - Also check: `HKEY_LOCAL_MACHINE\SOFTWARE\Python`

3. **Restart Computer**

4. **Fresh Install:**
   - Download latest Python from python.org
   - Run installer with "Add to PATH" checked
   - Choose "Install Now"

5. **Disable Microsoft Store Aliases** (see Quick Fix)

6. **Verify Installation** (see Verification Steps)

## Testing Your Setup with Fabazzz

Once Python is properly configured:

```powershell
# Clone repository (if not already cloned)
git clone <repository-url>
cd fabazzz-legal

# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Verify Python in venv
python --version
which python  # Should point to venv

# Install dependencies (when available)
pip install -r requirements.txt

# Run application (when available)
python main.py
```

## Additional Resources

- **Official Python Documentation:** https://docs.python.org/3/
- **Python on Windows Guide:** https://docs.python.org/3/using/windows.html
- **Virtual Environments Tutorial:** https://docs.python.org/3/tutorial/venv.html
- **pip Documentation:** https://pip.pypa.io/en/stable/
- **Windows Python Launcher:** https://docs.python.org/3/using/windows.html#python-launcher-for-windows

## Getting Help

If you continue experiencing issues:

1. Check Python version compatibility: `python --version`
2. Check pip version: `pip --version`
3. Verify PATH: `echo $env:PATH` (PowerShell) or `echo %PATH%` (CMD)
4. Test with Python launcher: `py --version`
5. Review error messages carefully
6. Search for specific error messages online
7. Open an issue in this repository with:
   - Your Python version
   - Your Windows version
   - Complete error message
   - Steps you've already tried

---

**Last Updated:** November 2025
