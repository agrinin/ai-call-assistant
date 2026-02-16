# Installation Guide

## Quick Installation (For End Users)

### Option 1: Use Pre-built Executable (Recommended)

1. **Download the executable**
   - Download `AI-Call-Assistant.exe` from the `dist` folder or GitHub releases
   - No installation needed - just run the .exe file

2. **Install Windows Phone Link** (if not already installed)
   - The app will detect if Phone Link is missing
   - Click "Install Phone Link" button in the app
   - Or manually: Open Microsoft Store → Search "Your Phone" → Install

3. **Pair Your Phone**
   - Open Phone Link on Windows
   - Follow on-screen instructions to pair your Android/iPhone
   - Enable Bluetooth on both devices

4. **Run the Application**
   - Double-click `AI-Call-Assistant.exe`
   - The app will automatically detect your phone connection

### Option 2: Build from Source

**Prerequisites:**
- Windows 10/11
- Python 3.8 or higher
- pip (Python package manager)

**Steps:**

1. **Clone or download the repository**
   ```bash
   git clone https://github.com/agrinin/ai-call-assistant.git
   cd ai-call-assistant
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Build the executable**
   ```bash
   python build_exe.py
   ```

4. **Run the application**
   - Navigate to `dist` folder
   - Run `AI-Call-Assistant.exe`

## Verification Checklist

After installation, verify:

- [ ] Application launches without errors
- [ ] Phone Link is detected (shows "Installed ✓")
- [ ] Phone connection is detected when connected
- [ ] "Launch Phone Link" button works
- [ ] "Make Call" function works with a test number

## Troubleshooting

### "Phone Link: Not Installed"
- Click "Install Phone Link" to open Microsoft Store
- Install "Your Phone" app
- Restart the application

### "Phone: Not Connected"
- Ensure Bluetooth is enabled on both devices
- Check Phone Link shows your phone as connected
- Try disconnecting and reconnecting
- Click "Refresh Status"

### Application Won't Start
- Ensure you have Windows 10/11
- Check Windows Defender isn't blocking the app
- Try running as Administrator (right-click → Run as administrator)

## System Requirements

- **OS**: Windows 10 (version 1809 or later) or Windows 11
- **RAM**: 4GB minimum (8GB recommended)
- **Storage**: 300MB free space
- **Bluetooth**: Required for phone connection
- **Phone**: Android 7.0+ or iPhone with iOS 14+

## Notes

- The executable is standalone - no Python installation needed for end users
- First run may take a few seconds to initialize
- Windows Defender may show a warning (false positive) - click "More info" → "Run anyway"

