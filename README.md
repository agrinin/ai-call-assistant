# AI Call Assistant - Version 1.0

A Windows application that integrates with Windows Phone Link to detect phone connections, access contacts, and make calls.

## Features (v1.0)

- ✅ Detect phone connection (USB or Bluetooth)
- ✅ Check Windows Phone Link installation status
- ✅ Launch Phone Link automatically
- ✅ Make calls through the application
- ✅ Basic contact access (enhanced in future versions)
- ✅ Real-time connection monitoring

## Requirements

- Windows 10/11
- Python 3.8 or higher (for building from source)
- Windows Phone Link (Your Phone) app installed
- Phone paired with Windows via Bluetooth or USB

## Installation

### Option 1: Use Pre-built Executable

1. Download `AI-Call-Assistant.exe` from the `dist` folder
2. Run the executable
3. If Phone Link is not installed, the app will prompt you to install it

### Option 2: Build from Source

1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd ai-call-assistant
   ```

2. Run the setup script:
   ```bash
   setup.bat
   ```

   Or manually:
   ```bash
   pip install -r requirements.txt
   python build_exe.py
   ```

3. The executable will be created in the `dist` folder

## First-Time Setup

### Manual Steps Required:

1. **Install Windows Phone Link** (if not already installed):
   - The app will detect if Phone Link is missing
   - Click "Install Phone Link" button in the app, OR
   - Manually open Microsoft Store and search for "Your Phone"
   - Install "Your Phone" (Phone Link) from the Microsoft Store
   - **Note**: Phone Link cannot be automatically installed - you must install it manually from the Store

2. **Pair Your Phone** (Manual Process):
   - Open Phone Link on your Windows PC (search "Phone Link" in Start menu)
   - Follow the on-screen instructions to pair your Android or iPhone
   - You'll need to:
     - Install "Phone Link" or "Link to Windows" app on your phone
     - Scan QR code or enter pairing code
     - Grant necessary permissions on your phone
   - Ensure Bluetooth is enabled on both devices

3. **Connect Your Phone**:
   - Once paired, your phone should automatically connect via Bluetooth
   - Or connect via USB cable (for data transfer, but calls use Bluetooth)
   - The app will detect the connection automatically

## Usage

1. Launch `AI-Call-Assistant.exe`

2. **Check Connection Status**:
   - The app will automatically detect if your phone is connected
   - Status is shown in the "Connection Status" section
   - Click "Refresh Status" to manually check

3. **Make a Call**:
   - Enter a phone number in the "Make Call" section
   - Click "Call"
   - Phone Link will handle the actual call

4. **Access Contacts**:
   - Click "Load Contacts" (limited in v1.0)
   - For full contact access, use Phone Link directly
   - Future versions will have better contact integration

## Technical Details

### Phone Link Integration

The app uses Windows URI schemes to interact with Phone Link:
- `ms-phone:` - Opens Phone Link
- `ms-phone-call:?PhoneNumber=XXX` - Initiates a call

### Connection Detection

- **Bluetooth**: Checks for active Bluetooth connections via PowerShell
- **USB**: Detects USB-connected phone devices via Windows PnP

### Limitations (v1.0)

- Contact access is limited (Phone Link doesn't expose a public API)
- No call transcription yet (coming in v2.0)
- No LLM assistance yet (coming in v2.0)
- Requires Phone Link to be installed separately

## Future Versions

- v2.0: Real-time call transcription using Whisper
- v3.0: LLM-powered call assistance and advice
- v4.0: Rule-based call coaching for customer service calls

## Legal Notice

⚠️ **Important**: This application may record or transcribe phone calls. Ensure you comply with local laws regarding call recording. In many jurisdictions (including Illinois), you must obtain consent from all parties before recording a conversation.

## Troubleshooting

### Phone Not Detected

1. Ensure Bluetooth is enabled on both devices
2. Check that Phone Link is running and phone is paired
3. Try disconnecting and reconnecting your phone
4. Restart the application

### Phone Link Won't Launch

1. Verify Phone Link is installed from Microsoft Store
2. Try launching Phone Link manually first
3. Check Windows updates

### Calls Not Working

1. Ensure Phone Link is paired and connected
2. Check that your phone has cellular service
3. Verify Bluetooth connection is active

## Development

### Project Structure

```
ai-call-assistant/
├── main.py              # Main application
├── requirements.txt     # Python dependencies
├── build_exe.py        # Build script
├── setup.bat           # Setup script for Windows
├── README.md           # This file
└── dist/               # Built executables (after build)
```

### Building

```bash
python build_exe.py
```

The executable will be created in `dist/AI-Call-Assistant.exe`

## License

[Add your license here]

## Contributing

[Add contribution guidelines if applicable]

