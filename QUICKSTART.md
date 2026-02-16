# Quick Start Guide

## Step 1: Install Dependencies

Run the setup script:
```bash
setup.bat
```

This will:
- Install Python dependencies
- Build the executable
- Check for Phone Link installation

## Step 2: Install Windows Phone Link (if needed)

If Phone Link is not installed:
1. The setup script will prompt you
2. Or manually open Microsoft Store and search for "Your Phone"
3. Install the app and follow the pairing instructions

## Step 3: Pair Your Phone

1. Open Phone Link on Windows
2. Follow the on-screen instructions
3. Enable Bluetooth on both devices
4. Complete the pairing process

## Step 4: Run the Application

1. Navigate to the `dist` folder
2. Run `AI-Call-Assistant.exe`
3. The app will automatically detect your phone connection

## Testing the Application

### Test 1: Connection Detection
- Connect your phone via Bluetooth or USB
- The app should show "Phone: Connected via [USB/Bluetooth] ✓"

### Test 2: Make a Call
- Enter a phone number (e.g., your own number for testing)
- Click "Call"
- Phone Link should open and initiate the call

### Test 3: Launch Phone Link
- Click "Launch Phone Link"
- Phone Link should open in a new window

## Troubleshooting

### "Phone Link: Not Installed"
- Click "Install Phone Link" button
- This opens Microsoft Store
- Install "Your Phone" app
- Restart the application

### "Phone: Not Connected"
- Ensure Bluetooth is enabled on both devices
- Check that Phone Link shows your phone as connected
- Try disconnecting and reconnecting
- Click "Refresh Status"

### Calls Not Working
- Ensure Phone Link is running
- Check that your phone has cellular service
- Verify the phone number format is correct

## Next Steps

Once v1.0 is working:
- v2.0 will add real-time transcription
- v3.0 will add LLM assistance

