# Fabazzz - TikTok Automation Tool

Fabazzz is an automation and content management application designed to interact with TikTok's official Developer API for scheduling posts, generating captions, and analyzing performance.

## Prerequisites

This application requires Python 3.8 or higher.

### Windows Python Installation

If you're seeing the error:
```
Python was not found; run without arguments to install from the Microsoft Store,
or disable this shortcut from Settings > Apps > Advanced app settings > App execution aliases.
```

This is a common Windows issue where the Microsoft Store Python stub is interfering with your Python installation. Follow the steps below to fix it.

## Fixing Python Path Issues on Windows

### Option 1: Disable Microsoft Store Python Alias (Recommended)

1. Open **Windows Settings** (Win + I)
2. Go to **Apps** → **Apps & features**
3. Click on **App execution aliases** (or **Advanced app options** → **App execution aliases**)
4. Find the entries for **App Installer python.exe** and **App Installer python3.exe**
5. Toggle both switches to **OFF**

### Option 2: Install Python and Add to PATH

1. **Download Python:**
   - Visit [python.org/downloads](https://www.python.org/downloads/)
   - Download Python 3.8 or higher

2. **Install Python:**
   - Run the installer
   - ✅ **IMPORTANT:** Check "Add Python to PATH" during installation
   - Choose "Customize installation" if you want to select specific features
   - Complete the installation

3. **Verify Installation:**
   ```powershell
   python --version
   # Should display: Python 3.x.x

   pip --version
   # Should display pip version
   ```

### Option 3: Manual PATH Configuration

If Python is installed but not in PATH:

1. Find your Python installation directory (usually `C:\Users\YourUsername\AppData\Local\Programs\Python\Python3xx\`)
2. Open **System Properties** → **Environment Variables**
3. Under **User variables** or **System variables**, find **Path**
4. Click **Edit** → **New**
5. Add these two paths:
   - `C:\Users\YourUsername\AppData\Local\Programs\Python\Python3xx\`
   - `C:\Users\YourUsername\AppData\Local\Programs\Python\Python3xx\Scripts\`
6. Click **OK** to save
7. **Restart** your terminal/PowerShell

## Verifying Python Installation

After fixing the PATH issue, verify Python is working:

```powershell
# Check Python version
python --version

# Check pip version
pip --version

# Test Python interpreter
python -c "print('Python is working!')"
```

## Installing Fabazzz Dependencies

Once Python is properly configured:

```bash
# Create a virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies (when requirements.txt is available)
pip install -r requirements.txt
```

## Troubleshooting

### "python is not recognized as an internal or external command"

- Ensure Python is added to PATH (see Option 2 or 3 above)
- Restart your terminal after modifying PATH
- Try using `py` instead of `python` (Windows Python Launcher)

### Multiple Python Versions Installed

If you have multiple Python versions:

```powershell
# Use Python Launcher to specify version
py -3.12 --version  # Use Python 3.12
py -3.8 --version   # Use Python 3.8

# List all installed Python versions
py --list
```

### Still Having Issues?

1. Completely uninstall Python
2. Restart your computer
3. Reinstall Python with "Add to PATH" checked
4. Disable Microsoft Store aliases (Option 1)

## Additional Resources

- [Python Official Documentation](https://docs.python.org/3/)
- [Windows Python Installation Guide](https://docs.python.org/3/using/windows.html)
- [Python Virtual Environments](https://docs.python.org/3/tutorial/venv.html)

## Support

For issues specific to Fabazzz, please open an issue in this repository.
