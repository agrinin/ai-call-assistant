"""
AI Call Assistant - First Version
Detects phone connections, accesses contacts, and makes calls via Windows Phone Link
"""

import sys
import os
import subprocess
import platform
import ctypes
from pathlib import Path
import json
from typing import List, Dict, Optional, Tuple
import threading
import time

try:
    import tkinter as tk
    from tkinter import ttk, messagebox, scrolledtext
except ImportError:
    print("tkinter not available. Please install Python with tkinter support.")
    sys.exit(1)

# Windows-specific imports
if platform.system() == "Windows":
    try:
        import winreg
    except ImportError:
        winreg = None
    
    try:
        import win32api
        import win32con
        from win32com.client import Dispatch
    except ImportError:
        # pywin32 not installed - some features may not work
        win32api = None
        win32con = None
        Dispatch = None


class PhoneLinkManager:
    """Manages Windows Phone Link integration"""
    
    PHONE_LINK_APP_ID = "Microsoft.YourPhone_8wekyb3d8bbwe"
    PHONE_LINK_EXE = "PhoneExperienceHost.exe"
    PHONE_LINK_URI = "ms-phone:"
    PHONE_CALL_URI = "ms-phone-call:"
    
    def __init__(self):
        self.phone_link_installed = False
        self.phone_connected = False
        self.connection_type = None  # "USB" or "Bluetooth"
        
    def check_phone_link_installed(self) -> bool:
        """Check if Windows Phone Link is installed"""
        try:
            # Method 1: Check via PowerShell Get-AppxPackage (most reliable)
            try:
                ps_command = "Get-AppxPackage -Name Microsoft.YourPhone | Select-Object -ExpandProperty Name"
                result = subprocess.run(
                    ["powershell", "-Command", ps_command],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                if "Microsoft.YourPhone" in result.stdout:
                    self.phone_link_installed = True
                    return True
            except:
                pass
            
            # Method 2: Check if Phone Link executable exists in WindowsApps
            try:
                windowsapps_path = os.path.expanduser(r"~\AppData\Local\Microsoft\WindowsApps")
                if os.path.exists(os.path.join(windowsapps_path, self.PHONE_LINK_EXE)):
                    self.phone_link_installed = True
                    return True
            except:
                pass
            
            # Method 3: Check if process is running
            try:
                result = subprocess.run(
                    ["tasklist", "/FI", f"IMAGENAME eq {self.PHONE_LINK_EXE}"],
                    capture_output=True,
                    text=True,
                    timeout=3
                )
                if self.PHONE_LINK_EXE.lower() in result.stdout.lower():
                    self.phone_link_installed = True
                    return True
            except:
                pass
            
            # Method 4: Try to verify URI scheme is registered
            try:
                # Check if ms-phone: URI is registered
                result = subprocess.run(
                    ["powershell", "-Command", "Get-ItemProperty -Path 'HKCU:\\Software\\Classes\\ms-phone' -ErrorAction SilentlyContinue"],
                    capture_output=True,
                    timeout=3
                )
                if result.returncode == 0:
                    self.phone_link_installed = True
                    return True
            except:
                pass
            
            self.phone_link_installed = False
            return False
        except Exception as e:
            print(f"Error checking Phone Link installation: {e}")
            self.phone_link_installed = False
            return False
    
    def install_phone_link(self) -> bool:
        """Attempt to install Windows Phone Link via Microsoft Store"""
        try:
            # Try to open Microsoft Store to Phone Link page
            store_uri = f"ms-windows-store://pdp/?ProductId=9NMPJ99TJBHZ"
            subprocess.Popen(["start", store_uri], shell=True)
            return True
        except Exception as e:
            print(f"Error opening Microsoft Store: {e}")
            return False
    
    def launch_phone_link(self) -> bool:
        """Launch Windows Phone Link application"""
        try:
            subprocess.Popen(["start", self.PHONE_LINK_URI], shell=True)
            return True
        except Exception as e:
            print(f"Error launching Phone Link: {e}")
            return False
    
    def check_bluetooth_connection(self) -> bool:
        """Check if Bluetooth is enabled and a device is connected"""
        try:
            # Use PowerShell to check Bluetooth status
            ps_command = """
            $adapters = Get-PnpDevice -Class Bluetooth | Where-Object {$_.Status -eq 'OK'}
            if ($adapters) {
                $devices = Get-PnpDevice -Class Bluetooth | Where-Object {$_.FriendlyName -like '*Phone*' -or $_.FriendlyName -like '*Mobile*'}
                if ($devices) { Write-Output 'CONNECTED' } else { Write-Output 'ENABLED' }
            } else {
                Write-Output 'DISABLED'
            }
            """
            result = subprocess.run(
                ["powershell", "-Command", ps_command],
                capture_output=True,
                text=True,
                timeout=5
            )
            output = result.stdout.strip()
            return "CONNECTED" in output or "ENABLED" in output
        except Exception as e:
            print(f"Error checking Bluetooth: {e}")
            return False
    
    def check_usb_connection(self) -> bool:
        """Check if phone is connected via USB"""
        try:
            # Check for Android devices or iPhone via USB
            ps_command = """
            Get-PnpDevice | Where-Object {
                ($_.Class -eq 'USB' -or $_.Class -eq 'WPD') -and 
                ($_.FriendlyName -like '*Android*' -or $_.FriendlyName -like '*iPhone*' -or $_.FriendlyName -like '*Phone*')
            } | Where-Object {$_.Status -eq 'OK'} | Select-Object -First 1
            """
            result = subprocess.run(
                ["powershell", "-Command", ps_command],
                capture_output=True,
                text=True,
                timeout=5
            )
            return len(result.stdout.strip()) > 0
        except Exception as e:
            print(f"Error checking USB connection: {e}")
            return False
    
    def detect_phone_connection(self) -> Tuple[bool, Optional[str]]:
        """Detect if phone is connected via USB or Bluetooth"""
        usb_connected = self.check_usb_connection()
        bluetooth_connected = self.check_bluetooth_connection()
        
        if usb_connected:
            self.phone_connected = True
            self.connection_type = "USB"
            return True, "USB"
        elif bluetooth_connected:
            self.phone_connected = True
            self.connection_type = "Bluetooth"
            return True, "Bluetooth"
        else:
            self.phone_connected = False
            self.connection_type = None
            return False, None
    
    def get_contacts_via_people_api(self) -> List[Dict]:
        """Get contacts using Windows People API (if available)"""
        contacts = []
        try:
            # Try using Windows Runtime API via Python
            # This requires pythonnet or similar, which is complex
            # For now, we'll use a simpler approach: try to access Phone Link's data
            # or use the People app URI
            
            # Alternative: Use Windows Contacts API via COM
            # This is a simplified version - full implementation would require more Windows API knowledge
            pass
        except Exception as e:
            print(f"Error getting contacts: {e}")
        
        return contacts
    
    def make_call(self, phone_number: str) -> bool:
        """Initiate a call using Phone Link"""
        try:
            # Remove any non-digit characters except +
            clean_number = ''.join(c for c in phone_number if c.isdigit() or c == '+')
            if not clean_number:
                return False
            
            # Use Phone Link URI scheme to make call
            call_uri = f"{self.PHONE_CALL_URI}?PhoneNumber={clean_number}"
            subprocess.Popen(["start", call_uri], shell=True)
            return True
        except Exception as e:
            print(f"Error making call: {e}")
            return False
    
    def make_call_to_contact(self, contact_name: str) -> bool:
        """Initiate a call to a contact by name"""
        # Phone Link URI scheme supports contact names
        try:
            call_uri = f"{self.PHONE_CALL_URI}?ContactName={contact_name}"
            subprocess.Popen(["start", call_uri], shell=True)
            return True
        except Exception as e:
            print(f"Error calling contact: {e}")
            return False


class CallAssistantApp:
    """Main application class"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("AI Call Assistant - v1.0")
        self.root.geometry("800x600")
        
        self.phone_manager = PhoneLinkManager()
        self.contacts = []
        self.monitoring = False
        
        self.setup_ui()
        self.check_initial_setup()
        
        # Start monitoring thread
        self.start_monitoring()
    
    def setup_ui(self):
        """Setup the user interface"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Status section
        status_frame = ttk.LabelFrame(main_frame, text="Connection Status", padding="10")
        status_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        self.status_label = ttk.Label(status_frame, text="Checking...", font=("Arial", 10, "bold"))
        self.status_label.grid(row=0, column=0, sticky=tk.W)
        
        self.connection_label = ttk.Label(status_frame, text="Phone: Not Connected", font=("Arial", 9))
        self.connection_label.grid(row=1, column=0, sticky=tk.W, pady=2)
        
        self.phone_link_label = ttk.Label(status_frame, text="Phone Link: Checking...", font=("Arial", 9))
        self.phone_link_label.grid(row=2, column=0, sticky=tk.W, pady=2)
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        
        self.refresh_btn = ttk.Button(button_frame, text="Refresh Status", command=self.refresh_status)
        self.refresh_btn.grid(row=0, column=0, padx=5)
        
        self.launch_phone_link_btn = ttk.Button(button_frame, text="Launch Phone Link", command=self.launch_phone_link)
        self.launch_phone_link_btn.grid(row=0, column=1, padx=5)
        
        self.install_phone_link_btn = ttk.Button(button_frame, text="Install Phone Link", command=self.install_phone_link)
        self.install_phone_link_btn.grid(row=0, column=2, padx=5)
        
        # Contacts section
        contacts_frame = ttk.LabelFrame(main_frame, text="Contacts", padding="10")
        contacts_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        # Contacts list
        contacts_list_frame = ttk.Frame(contacts_frame)
        contacts_list_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        scrollbar = ttk.Scrollbar(contacts_list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.contacts_listbox = tk.Listbox(contacts_list_frame, yscrollcommand=scrollbar.set, height=10)
        self.contacts_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.contacts_listbox.yview)
        
        # Bind double-click to call
        self.contacts_listbox.bind('<Double-1>', self.on_contact_double_click)
        
        # Load contacts button
        load_contacts_btn = ttk.Button(contacts_frame, text="Load Contacts", command=self.load_contacts)
        load_contacts_btn.grid(row=1, column=0, pady=5)
        
        # Make call section
        call_frame = ttk.LabelFrame(main_frame, text="Make Call", padding="10")
        call_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Label(call_frame, text="Phone Number:").grid(row=0, column=0, sticky=tk.W, padx=5)
        self.phone_entry = ttk.Entry(call_frame, width=20)
        self.phone_entry.grid(row=0, column=1, padx=5)
        
        call_btn = ttk.Button(call_frame, text="Call", command=self.make_call)
        call_btn.grid(row=0, column=2, padx=5)
        
        # Log section
        log_frame = ttk.LabelFrame(main_frame, text="Log", padding="10")
        log_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=8, width=70)
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)
        main_frame.rowconfigure(4, weight=1)
        contacts_frame.columnconfigure(0, weight=1)
        contacts_frame.rowconfigure(0, weight=1)
    
    def log(self, message: str):
        """Add message to log"""
        self.log_text.insert(tk.END, f"[{time.strftime('%H:%M:%S')}] {message}\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()
    
    def check_initial_setup(self):
        """Check initial setup and update UI"""
        self.log("Checking Phone Link installation...")
        phone_link_installed = self.phone_manager.check_phone_link_installed()
        
        if phone_link_installed:
            self.phone_link_label.config(text="Phone Link: Installed ✓", foreground="green")
            self.log("Phone Link is installed")
        else:
            self.phone_link_label.config(text="Phone Link: Not Installed ✗", foreground="red")
            self.log("Phone Link is not installed")
            messagebox.showwarning(
                "Phone Link Not Found",
                "Windows Phone Link is not installed.\n\n"
                "Click 'Install Phone Link' to open Microsoft Store and install it.\n\n"
                "Phone Link is required for this application to work."
            )
        
        self.refresh_status()
    
    def refresh_status(self):
        """Refresh connection status"""
        self.log("Checking phone connection...")
        connected, connection_type = self.phone_manager.detect_phone_connection()
        
        if connected:
            self.connection_label.config(
                text=f"Phone: Connected via {connection_type} ✓",
                foreground="green"
            )
            self.status_label.config(text="Status: Ready", foreground="green")
            self.log(f"Phone detected via {connection_type}")
        else:
            self.connection_label.config(
                text="Phone: Not Connected ✗",
                foreground="red"
            )
            self.status_label.config(text="Status: Waiting for phone...", foreground="orange")
            self.log("No phone connection detected")
    
    def launch_phone_link(self):
        """Launch Windows Phone Link"""
        self.log("Launching Phone Link...")
        if self.phone_manager.launch_phone_link():
            self.log("Phone Link launched successfully")
            messagebox.showinfo("Success", "Phone Link has been launched.\n\nPlease pair your phone if not already done.")
        else:
            self.log("Failed to launch Phone Link")
            messagebox.showerror("Error", "Failed to launch Phone Link.\n\nPlease install it from Microsoft Store.")
    
    def install_phone_link(self):
        """Install Windows Phone Link"""
        self.log("Opening Microsoft Store to install Phone Link...")
        if self.phone_manager.install_phone_link():
            self.log("Microsoft Store opened")
            messagebox.showinfo(
                "Install Phone Link",
                "Microsoft Store has been opened.\n\n"
                "Please install 'Your Phone' (Phone Link) from the Store.\n\n"
                "After installation, restart this application."
            )
        else:
            self.log("Failed to open Microsoft Store")
            messagebox.showerror("Error", "Failed to open Microsoft Store.")
    
    def load_contacts(self):
        """Load contacts (placeholder - will be enhanced)"""
        self.log("Loading contacts...")
        # For now, we'll show a message that contacts need to be accessed via Phone Link
        # Full contact access requires more complex Windows API integration
        self.contacts_listbox.delete(0, tk.END)
        self.log("Note: Full contact access requires Phone Link to be running and phone to be paired.")
        self.log("For now, you can make calls by entering phone numbers directly.")
        
        # Try to get contacts via People API (if available)
        contacts = self.phone_manager.get_contacts_via_people_api()
        if contacts:
            for contact in contacts:
                self.contacts_listbox.insert(tk.END, contact.get('name', 'Unknown'))
            self.log(f"Loaded {len(contacts)} contacts")
        else:
            self.log("Could not access contacts directly. Use Phone Link to view contacts.")
            messagebox.showinfo(
                "Contacts",
                "Direct contact access is limited.\n\n"
                "Please use Phone Link to view your contacts, or enter phone numbers manually.\n\n"
                "This feature will be enhanced in future versions."
            )
    
    def on_contact_double_click(self, event):
        """Handle double-click on contact"""
        selection = self.contacts_listbox.curselection()
        if selection:
            contact_name = self.contacts_listbox.get(selection[0])
            self.log(f"Calling {contact_name}...")
            if self.phone_manager.make_call_to_contact(contact_name):
                self.log(f"Call initiated to {contact_name}")
            else:
                self.log(f"Failed to call {contact_name}")
                messagebox.showerror("Error", f"Failed to call {contact_name}")
    
    def make_call(self):
        """Make a call to the entered phone number"""
        phone_number = self.phone_entry.get().strip()
        if not phone_number:
            messagebox.showwarning("Warning", "Please enter a phone number")
            return
        
        self.log(f"Calling {phone_number}...")
        if self.phone_manager.make_call(phone_number):
            self.log(f"Call initiated to {phone_number}")
            messagebox.showinfo("Call", f"Calling {phone_number}...\n\nPhone Link should open to handle the call.")
        else:
            self.log(f"Failed to call {phone_number}")
            messagebox.showerror("Error", f"Failed to call {phone_number}")
    
    def start_monitoring(self):
        """Start background monitoring of phone connection"""
        self.monitoring = True
        
        def monitor():
            while self.monitoring:
                time.sleep(5)  # Check every 5 seconds
                if self.monitoring:
                    connected, connection_type = self.phone_manager.detect_phone_connection()
                    current_text = self.connection_label.cget("text")
                    expected_text = f"Phone: Connected via {connection_type} ✓" if connected else "Phone: Not Connected ✗"
                    
                    if current_text != expected_text:
                        self.root.after(0, self.refresh_status)
        
        monitor_thread = threading.Thread(target=monitor, daemon=True)
        monitor_thread.start()


def main():
    """Main entry point"""
    # Check if running on Windows
    if platform.system() != "Windows":
        print("This application is designed for Windows only.")
        sys.exit(1)
    
    root = tk.Tk()
    app = CallAssistantApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()

